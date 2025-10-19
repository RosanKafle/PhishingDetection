#!/usr/bin/env python3
"""
Run the phishing_detection training/script and render a small dashboard image (PNG).
This script is resilient: uses matplotlib with 'Agg' backend when available, and falls
back to Pillow (PIL) if matplotlib isn't installed.
Prints a single JSON object to stdout with keys: metrics, image (path), stdout, stderr
"""

import json
import os
import sys
import subprocess
from io import BytesIO

# repo root = two levels up from this script (backend/scripts -> backend -> repo)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Paths
script_path = os.path.join(project_root, 'phishing_detection.py')
out_dir = os.path.join(project_root, 'backend', 'data')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'ml_dashboard.png')

_HAS_MATPLOTLIB = False
_HAS_PIL = False
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    _HAS_MATPLOTLIB = True
except Exception:
    plt = None
    try:
        from PIL import Image, ImageDraw, ImageFont
        _HAS_PIL = True
    except Exception:
        Image = ImageDraw = ImageFont = None

def parse_metrics_from_stdout(stdout):
    metrics = {}
    for line in stdout.splitlines():
        if line.startswith('Accuracy:'):
            metrics['accuracy'] = line.split(':',1)[1].strip()
        elif line.startswith('Precision:'):
            metrics['precision'] = line.split(':',1)[1].strip()
        elif line.startswith('Recall:'):
            metrics['recall'] = line.split(':',1)[1].strip()
        elif line.startswith('F1-Score:'):
            metrics['f1'] = line.split(':',1)[1].strip()
    return metrics

def to_float_percent(s):
    try:
        return float(str(s).strip().rstrip('%'))
    except Exception:
        return 0.0

def _render_matplotlib_chart(labels, values):
    """Render chart using matplotlib"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10,6), facecolor='#1a1a1a')
    ax.set_facecolor('#1a1a1a')
    
    colors = ['#00d4aa', '#0ea5e9', '#f59e0b', '#ec4899']
    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='white', linewidth=0.5)
    
    # Modern styling
    ax.set_ylim(0,100)
    ax.set_ylabel('Performance (%)', color='white', fontsize=12)
    ax.set_title('ML Model Performance Dashboard', color='white', fontsize=16, fontweight='bold', pad=20)
    ax.tick_params(colors='white', labelsize=10)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, color='white')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
               f'{value:.1f}%', ha='center', va='bottom', color='white', fontweight='bold')
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', facecolor='#1a1a1a', dpi=150)
    plt.close(fig)
    return buf

def _render_pil_chart(labels, values):
    """Render chart using PIL as fallback"""
    width, height = 600, 300
    margin = 40
    num = len(values)
    spacing = (width - 2*margin) / num
    bar_w = int(spacing * 0.6)
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 14)
    except Exception:
        font = ImageFont.load_default() if ImageFont is not None else None
    
    max_h = height - 2*margin
    colors = ['#4caf50','#2196f3','#ff9800','#9c27b0']
    
    for i, v in enumerate(values):
        x = int(margin + i * spacing + (spacing - bar_w) / 2)
        bar_h = int((v / 100.0) * max_h)
        y0 = height - margin - bar_h
        y1 = height - margin
        draw.rectangle([x, y0, x + bar_w, y1], fill=colors[i % len(colors)])
        
        txt = f"{v:.1f}%"
        if font is not None:
            tw, th = draw.textsize(txt, font=font)
        else:
            tw = th = 0
        draw.text((x, max(y0 - th - 4, 0)), txt, fill='black', font=font)
        
        lbl = labels[i]
        if font is not None:
            lw, lh = draw.textsize(lbl, font=font)
        draw.text((x, y1 + 4), lbl, fill='black', font=font)
    
    title = 'Phishing Detector Metrics'
    if font is not None:
        tw, th = draw.textsize(title, font=font)
    draw.text((margin, 8), title, fill='black', font=font)
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf

def render_image(metrics):
    labels = ['Accuracy', 'Precision', 'Recall', 'F1']
    values = [to_float_percent(metrics.get('accuracy','0')), to_float_percent(metrics.get('precision','0')), to_float_percent(metrics.get('recall','0')), to_float_percent(metrics.get('f1','0'))]
    
    buf = None
    if _HAS_MATPLOTLIB and plt is not None:
        buf = _render_matplotlib_chart(labels, values)
    elif _HAS_PIL and Image is not None:
        buf = _render_pil_chart(labels, values)
    
    if buf:
        buf.seek(0)
        with open(out_path, 'wb') as f:
            f.write(buf.read())
        return True
    else:
        # Can't render - write empty file
        with open(out_path, 'wb') as f:
            f.write(b'')
        return False

def main():
    if not os.path.exists(script_path):
        print(json.dumps({'error': 'phishing_detection.py not found'}))
        return
    
    try:
        proc = subprocess.run(
            [sys.executable, script_path], 
            capture_output=True, 
            text=True, 
            timeout=120,  # Reduced timeout for better performance
            cwd=project_root
        )
        
        stdout = proc.stdout or ''
        stderr = proc.stderr or ''
        metrics = parse_metrics_from_stdout(stdout)
        
        # Render image
        rendered = render_image(metrics)
        result = {
            'metrics': metrics, 
            'image': out_path if rendered else None, 
            'stdout': stdout, 
            'stderr': stderr
        }
        print(json.dumps(result))
        
    except subprocess.TimeoutExpired:
        print(json.dumps({'error': 'Script execution timeout'}))
    except Exception as e:
        print(json.dumps({'error': str(e)}))

if __name__ == '__main__':
    main()

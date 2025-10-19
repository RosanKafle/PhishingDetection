const { spawn } = require('child_process');
const path = require('path');

function runPythonWithInput(scriptName, inputObj) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '../../', scriptName);
    const py = spawn('python3', [scriptPath], { cwd: path.dirname(scriptPath) });
    let out = '';
    let err = '';
    py.stdout.on('data', d => out += d);
    py.stderr.on('data', d => err += d);
    py.on('close', code => {
      if (code !== 0 || err) return reject(new Error(err || `Exit code ${code}`));
      try { const parsed = JSON.parse(out); resolve(parsed); } catch (e) { reject(e); }
    });
    py.stdin.write(JSON.stringify(inputObj));
    py.stdin.end();
  });
}

module.exports = { runPythonWithInput };

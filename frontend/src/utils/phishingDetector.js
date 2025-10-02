export const detectPhishing = (content) => {
  const suspiciousPatterns = [
    { regex: /\b(http|https):\/\/\d{1,3}(?:\.\d{1,3}){3}\b/, reason: 'IP address in URL' },
    { regex: /(account|verify|urgent|suspend|password|invoice|payment|login|reset)/i, reason: 'Suspicious keywords' },
    { regex: /@[^\s]+\.[a-z]{2,}/i, reason: 'Mentions of email-like patterns' },
    { regex: /(tinyurl\.com|bit\.ly|goo\.gl|t\.co|ow\.ly)/i, reason: 'URL shortener detected' },
    { regex: /(\b\d{4}\b[ -]?){3}\d{4}/, reason: 'Possible credit card pattern' }
  ];

  const heuristics = [
    {
      test: (text) => /click\s+(here|now)/i.test(text) && /(update|verify|confirm)/i.test(text),
      reason: 'Urgent call-to-action with click here'
    },
    {
      test: (text) => /\bprize\b|\bwon\b|\bcongratulations\b/i.test(text) && /provide|send|share/i.test(text),
      reason: 'Prize lure with request for info'
    }
  ];

  for (const pattern of suspiciousPatterns) {
    if (pattern.regex.test(content)) {
      return { isPhishing: true, reason: pattern.reason };
    }
  }

  for (const rule of heuristics) {
    if (rule.test(content)) {
      return { isPhishing: true, reason: rule.reason };
    }
  }

  return { isPhishing: false, reason: 'No suspicious patterns found' };
};
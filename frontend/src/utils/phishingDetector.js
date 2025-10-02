export const detectPhishing = (content) => {
  const suspiciousPatterns = [
    { regex: /\b(http|https):\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, reason: 'IP address in URL' },
    { regex: /phish|bank|paypal|login|update password/i, reason: 'Suspicious keywords' }
  ];

  for (const pattern of suspiciousPatterns) {
    if (pattern.regex.test(content)) {
      return { isPhishing: true, reason: pattern.reason };
    }
  }

  return { isPhishing: false, reason: 'No suspicious patterns found' };
};
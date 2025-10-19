export const setAuthToken = (token) => localStorage.setItem('token', token);
export const getAuthToken = () => localStorage.getItem('token');
export const removeAuthToken = () => localStorage.removeItem('token');

export const isAdmin = () => {
  const token = getAuthToken();
  if (!token) return false;
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return false;
    const payload = JSON.parse(atob(parts[1]));
    return payload.username === 'admin' || payload.role === 'admin';
  } catch (error) {
    console.warn('Token validation failed:', error.message);
    removeAuthToken(); // Clear invalid token
    return false;
  }
};
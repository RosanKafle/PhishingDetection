import axios from 'axios';

export async function runPythonScript(script, args = []) {
  try {
    const response = await axios.post('/api/python/run', {
      script,
      args
    });
    return response.data;
  } catch (error) {
    return { error: error.message };
  }
}

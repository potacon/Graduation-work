import axios from 'axios';

const API_URL = 'http://localhost:8000'; // replace with your Flask server URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
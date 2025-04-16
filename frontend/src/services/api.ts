import axios from 'axios';

// Get the API base URL from environment variables
// Vite uses import.meta.env for env variables
// VITE_API_BASE_URL needs to be set in a .env file in the frontend directory
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor later (TASK-204.11) to include auth token
// apiClient.interceptors.request.use(...);

export default apiClient; 
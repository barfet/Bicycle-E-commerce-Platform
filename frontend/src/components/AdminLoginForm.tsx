import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../services/api';

const AdminLoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null); // Clear previous errors
    setLoading(true);

    try {
      const response = await apiClient.post('/admin/login', {
        username,
        password,
      });

      const { access_token } = response.data; // Assuming backend returns { access_token: ..., token_type: ... }

      if (access_token) {
        // Store the token (TASK-204.7)
        localStorage.setItem('admin_token', access_token);
        // Redirect to admin dashboard (TASK-204.8)
        navigate('/admin/dashboard');
      } else {
        setError('Login failed: No token received.');
      }

    } catch (err: any) {
      // Handle login errors (TASK-204.9)
      if (err.response && err.response.status === 401) {
        setError('Invalid username or password.');
      } else {
        setError('Login failed. Please try again later.');
        console.error("Login error:", err);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', maxWidth: '300px', gap: '1rem' }}>
      <h2>Admin Login</h2>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem' }}
        />
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit" disabled={loading} style={{ padding: '0.75rem' }}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

export default AdminLoginForm; 
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LoginPageManager() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    login({ username, password });
    navigate('/managerdashboard');
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Manager Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label><br />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div style={{ marginTop: '0.5rem' }}>
          <label>Password:</label><br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" style={{ marginTop: '1rem' }}>
          Login
        </button>
      </form>
      {/* Return Home Button */}
      <button
        onClick={() => navigate('/')}
        style={{ marginTop: '1rem', backgroundColor: '#ccc' }}
      >
        Return Home
      </button>
    </div>
  );
}

export default LoginPageManager;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    login({ username, password });
    navigate('/managerdashboard');
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Login Manager</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: 300 }}>
        <div>
          <label>Username</label><br />
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            type="text"
          />
        </div>
        <div style={{ marginTop: '0.5rem' }}>
          <label>Password</label><br />
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
          />
        </div>
        <button type="submit" style={{ marginTop: '1rem' }}>Log In</button>
      </form>
    </div>
  );
}

export default LoginPage;

import React from 'react';
import { useAuth } from '../context/AuthContext';
import ChatbotInterface from '../components/ChatbotInterface';
import dashboard from '../dashboard.png';

function DashboardPage() {
  const { isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) {
    return <p>You must be logged in to see this page.</p>;
  }

  return (
    <div style={{ padding: '1rem' }}>
      <h2 style = {{marginTop: 30}}>Dashboard</h2>
      <p style = {{fontFamily: "Gill Sans"}}>View your company's AI adoption rate here:</p>
      
      <div style={{ marginBottom: '1rem', marginLeft: 0, backgroundColor: 'white', width: '870px', height: '550px', overflowY: 'auto', padding: '1rem', 
        position: 'absolute'
      }}>
      <a>
        <img src = {dashboard} alt = 'dashboard' style={{ width: '880px'}}/> 
        </a>

      </div>

      <div style={{}}>
        <ChatbotInterface />
      </div>

      <button onClick={logout} style={{ marginTop: 630 }}>
        Logout
      </button>
    </div>
  );
}

export default DashboardPage;


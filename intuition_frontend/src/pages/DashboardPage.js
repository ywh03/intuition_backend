import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './DashboardPage.css';

const aiTools = {
  Ideation: [
    {
      name: 'SparkBeyond',
      description: 'AI-powered research and insight generation platform.',
      link: 'https://www.sparkbeyond.com',
    },
    {
      name: 'ChatGPT',
      description: 'Brainstorm and generate creative design concepts.',
      link: 'https://chat.openai.com',
    },
  ],
  Designing: [
    {
      name: 'Fusion 360 Generative Design',
      description: 'AI-driven generative design platform by Autodesk.',
      link: 'https://www.autodesk.com/solutions/generative-design',
    },
    {
      name: 'nTopology',
      description: 'Advanced computational design for engineers.',
      link: 'https://ntopology.com',
    },
  ],
  Prototyping: [
    {
      name: 'Ansys Discovery',
      description: 'Real-time simulation and rapid prototyping design.',
      link: 'https://www.ansys.com/products/discovery',
    },
    {
      name: 'SolidWorks 3DEXPERIENCE',
      description: 'Simulation-driven design and validation.',
      link: 'https://www.solidworks.com',
    },
  ],
  Testing: [
    {
      name: 'Landing AI',
      description: 'Computer vision platform for defect detection.',
      link: 'https://landing.ai',
    },
    {
      name: 'Instrumental.ai',
      description: 'AI for root cause analysis and failure detection.',
      link: 'https://www.instrumental.com',
    },
  ],
};

function RatingPopup({ onRate }) {
  return (
    <div style={styles.popupOverlay}>
      <div style={styles.popupContainer}>
        <h3>Please rate your experience</h3>
        <div style={styles.ratingButtons}>
          <button
            style={{ ...styles.ratingButton, backgroundColor: 'red' }}
            onClick={() => onRate('red')}
          >
            Poor
          </button>
          <button
            style={{ ...styles.ratingButton, backgroundColor: '#edc80c'}}
            onClick={() => onRate('yellow')}
          >
            Moderate
          </button>
          <button
            style={{ ...styles.ratingButton, backgroundColor: 'green' }}
            onClick={() => onRate('green')}
          >
            Good
          </button>
        </div>
      </div>
    </div>
  );
}

function DashboardPage() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [selectedStage, setSelectedStage] = useState(null);
  const [showRatingPopup, setShowRatingPopup] = useState(false);

  // Check for "needRating" flag on mount and whenever the document becomes visible
  useEffect(() => {
    const checkRating = () => {
      if (localStorage.getItem('needRating') === 'true') {
        setShowRatingPopup(true);
      }
    };

    // Check on mount
    checkRating();

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        checkRating();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/'); // Return to home page
  };

  const handleRating = (rating) => {
    console.log('User rating:', rating);
    setShowRatingPopup(false);
    localStorage.removeItem('needRating');
  };

  return (
    <div style={{ padding: '2rem' }}>
      {/* Rating Popup Modal */}
      {showRatingPopup && <RatingPopup onRate={handleRating} />}

      {/* Header with Title and Logout Button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Dashboard</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ color: '#666' }}>Logged in as: Manufacturing001</span>
          <button
              onClick={handleLogout}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: '#007bff',
                color: '#fff',
                border: 'none',
                borderRadius: '4px',
              }}
          >
            Logout
          </button>
        </div>
      </div>
      <p>Select a stage to explore AI tools:</p>

      {/* Timeline Layout */}
      <div className="timeline">
        {['Ideation', 'Designing', 'Prototyping', 'Testing'].map((stage) => (
          <div
            key={stage}
            className={`timeline-box ${selectedStage === stage ? 'active' : ''}`}
            onClick={() => setSelectedStage(stage)}
          >
            {stage}
          </div>
        ))}
      </div>

      {/* Tool List Display */}
      {selectedStage && (
        <div className="tool-list">
          <h3>{selectedStage} – AI Tools</h3>
          <ul>
            {aiTools[selectedStage].map((tool) => (
              <li key={tool.name} style={{ marginBottom: '1rem' }}>
                <a
                  href={tool.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  // Set flag when link is clicked so that a rating popup shows on return
                  onClick={() => localStorage.setItem('needRating', 'true')}
                >
                  <strong>{tool.name}</strong>
                </a>
                <p>{tool.description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const styles = {
  popupOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 10000,
  },
  popupContainer: {
    backgroundColor: '#fff',
    padding: '2rem',
    borderRadius: '8px',
    textAlign: 'center',
    width: '300px',
  },
  ratingButtons: {
    display: 'flex',
    justifyContent: 'space-around',
    marginTop: '1rem',
  },
  ratingButton: {
    padding: '0.5rem 1rem',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer',
  },
};

export default DashboardPage;

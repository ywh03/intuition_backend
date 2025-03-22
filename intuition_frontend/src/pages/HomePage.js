import React from 'react';
import './HomePage.css';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const navigate = useNavigate();
  const handleSubmit1 = (e) => {
    e.preventDefault();
    navigate('/login');
  };
  const handleSubmit2 = (e) => {
    e.preventDefault();
    navigate('/loginmanager');
  };

  return (
    <div style={{display: 'flex', flexDirection: 'column', height: 'calc(100vh - 50.5px)', justifyContent: 'flex-end'}}>
      <div style = {{
      backgroundColor: 'white',
      alignSelf: 'end',
      width: '100%',
      height: 120,
      opacity: 0.7,
      alignItems: 'center',
      justifyContent: 'space-evenly',
      display: 'flex',
    }} >
      <form onSubmit={handleSubmit1}>
        <button type="submit" style={{fontSize: '2rem', width: '400px', padding: '10px', borderRadius: '20px',
                                    fontFamily: "Gill Sans", backgroundColor: '#91c7c9', opacity: 1}}>EMPLOYEE LOGIN</button>
      </form>

      <form onSubmit={handleSubmit2}>
        <button type="submit" style={{fontSize: '2rem', width: '400px', padding: '10px', borderRadius: '20px',
                                    fontFamily: "Gill Sans", backgroundColor: '#91c7c9', opacity: 1}}>MANAGER LOGIN</button>
      </form>

      </div>
      
    
  </div>
  );
}

export default HomePage;
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './Home.css';

function Home() {
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const handleOptionSelection = (option) => {
    if (option === 'text') {
      navigate('/text-summary'); // Navigate to Text Summary page
    } else if (option === 'video') {
      navigate('/video-summary'); // Navigate to Video Summary page
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <div className="home-container">
      <div className="home-box">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>Welcome to Concisely, {user}!</h2>
          <button onClick={handleLogout} style={{ padding: '8px 16px', cursor: 'pointer' }}>Logout</button>
        </div>
        <p>Choose an option to proceed:</p>
        <div className="option-buttons">
          <button onClick={() => handleOptionSelection('text')}>Summarize Text</button>
          <button onClick={() => handleOptionSelection('video')}>Summarize Video</button>
        </div>
      </div>
    </div>
  );
}

export default Home;

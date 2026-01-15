import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './ProtectedRoute';
import Landing from './Landing';
import Signup from './Signup';
import Login from './Login';
import Home from './Home';
import TextSummary from './TextSummary';
import VideoSummary from './VideoSummary';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route 
              path="/home" 
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/text-summary" 
              element={
                <ProtectedRoute>
                  <TextSummary />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/video-summary" 
              element={
                <ProtectedRoute>
                  <VideoSummary />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

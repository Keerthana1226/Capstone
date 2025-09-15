import React from 'react';
// ⬇️ 1. Import the Link component ⬇️
import { Link } from 'react-router-dom';
// You may have a CSS file for HomePage, import it if you do
// import './HomePage.css'; 

function HomePage() {
  return (
    <div className="container mt-5">
      <div className="text-center mb-5">
        <h1>Smart Farming Assistant</h1>
      </div>

      {/* This row will hold all the feature cards */}
      <div className="row justify-content-center g-4">

        {/* Card 1: Crop Rotation (Existing) */}
        <div className="col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body text-center">
              <h5 className="card-title">Crop Rotation</h5>
              <p className="card-text">Generate AI-based crop rotation plans for sustainable farming.</p>
              <Link to="/rotation" className="btn btn-success">Launch</Link>
            </div>
          </div>
        </div>

        {/* Card 2: Companion Planting (Existing) */}
        <div className="col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body text-center">
              <h5 className="card-title">Companion Planting</h5>
              <p className="card-text">View crops and their ideal companion plants.</p>
              {/* Assuming this links to your crops list */}
              <Link to="/crops" className="btn btn-primary">Launch</Link>
            </div>
          </div>
        </div>

        {/* Card 3: Crop Recommendation (Existing) */}
        <div className="col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body text-center">
              <h5 className="card-title">Crop Recommendation</h5>
              <p className="card-text">Enter soil and weather data to get a recommended crop.</p>
              <Link to="/crop-recommend" className="btn btn-warning">Launch</Link>
            </div>
          </div>
        </div>

        {/* ⬇️ 2. ADD THE NEW CARD FOR DISEASE DETECTION HERE ⬇️ */}
        <div className="col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body text-center">
              <h5 className="card-title">Disease Detection</h5>
              <p className="card-text">Upload an image of a plant leaf to detect potential diseases.</p>
              <Link to="/disease-detection" className="btn btn-danger">Launch</Link>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default HomePage;
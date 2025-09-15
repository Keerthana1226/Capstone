import React, { useState } from 'react';
import axios from 'axios';

function CropRotationPage() {
  const [lastCrop, setLastCrop] = useState('');
  const [month, setMonth] = useState('');
  const [season, setSeason] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setRecommendations([]);

    if ((month && season) || (!month && !season)) {
      setError('Please enter either the month or the season, but not both.');
      return;
    }

    try {
      const payload = {
        last_crop: lastCrop,
        ...(month && { month: parseInt(month) }),
        ...(season && { season })
      };

      const res = await axios.post('http://localhost:5000/api/rotation-plan/run-recommendation', payload);

      const mapped = res.data.recommendations.map((rec) => ({
        crop: rec.crop || 'Unknown Crop',
        planting_months: rec.planting_months || [],
        grow_duration: rec.grow_duration || 'N/A',
        successor_crops: rec.successor_crops || [],
        confidence: rec.confidence || 0
      }));

      setRecommendations(mapped);

      if (res.data.message) {
        setMessage(res.data.message);
      }
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      if (err.response && err.response.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('Failed to fetch recommendations.');
      }
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="mb-4">🌿 Smart Crop Recommendation</h1>

      <form onSubmit={handleSubmit} className="mb-4">
        <div className="form-group mb-3">
          <label>Last Planted Crop</label>
          <input
            type="text"
            className="form-control"
            placeholder="e.g., Rice"
            value={lastCrop}
            onChange={(e) => setLastCrop(e.target.value)}
          />
        </div>

        <div className="form-group mb-3">
          <label>Current Month (1–12)</label>
          <input
            type="number"
            className="form-control"
            placeholder="e.g., 7"
            min="1"
            max="12"
            value={month}
            onChange={(e) => {
              setMonth(e.target.value);
              if (e.target.value) setSeason('');
            }}
          />
        </div>

        <div className="form-group mb-3">
          <label>OR Current Season</label>
          <select
            className="form-control"
            value={season}
            onChange={(e) => {
              setSeason(e.target.value);
              if (e.target.value) setMonth('');
            }}
          >
            <option value="">-- Select Season (optional) --</option>
            <option value="Spring">Spring</option>
            <option value="Summer">Summer</option>
            <option value="Fall">Fall</option>
            <option value="Winter">Winter</option>
          </select>
        </div>

        <button type="submit" className="btn btn-success">Get Recommendations</button>
      </form>

      {error && <div className="alert alert-danger">{error}</div>}
      {message && <div className="alert alert-warning">{message}</div>}

      {recommendations.length > 0 && (
        <div>
          <h3>✅ Recommended Crops:</h3>
          {recommendations.map((rec, index) => (
            <div key={index} className="card mb-3">
              <div className="card-body">
                <h5 className="card-title">{rec.crop}</h5>
                <p className="card-text"><strong>Confidence:</strong> {rec.confidence.toFixed(2)}</p>
                <p className="card-text"><strong>Planting Months:</strong> {rec.planting_months.join(', ') || 'N/A'}</p>
                <p className="card-text"><strong>Grow Duration:</strong> {rec.grow_duration} months</p>
                <p className="card-text"><strong>Successor Crops:</strong> {rec.successor_crops.join(', ') || 'N/A'}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CropRotationPage;

import React, { useState } from 'react';
import axios from 'axios';

function CropRecommendation() {
  const [formData, setFormData] = useState({
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:5000/api/crop-recommend', formData);
      setResult(response.data.predicted_crop);
    } catch (err) {
      console.error(err);
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">🌾 Crop Recommendation Tool</h2>

      <form onSubmit={handleSubmit} className="row g-3">
        {Object.keys(formData).map((key) => (
          <div key={key} className="col-md-6">
            <label className="form-label text-capitalize">{key}</label>
            <input
              type="number"
              className="form-control"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <div className="col-12">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Predicting...' : 'Recommend Crop'}
          </button>
        </div>
      </form>

      {result && (
        <div className="alert alert-success mt-4">
          🌱 Recommended Crop: <strong>{result}</strong>
        </div>
      )}

      {error && <div className="alert alert-danger mt-4">{error}</div>}
    </div>
  );
}

export default CropRecommendation;
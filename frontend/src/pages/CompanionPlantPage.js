import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function CompanionPlantPage() {
  const { id } = useParams(); // Get crop ID from URL
  const [crop, setCrop] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:5000/api/crops/${id}`)
      .then((res) => {
        setCrop(res.data);
      })
      .catch((err) => {
        console.error('Error fetching crop details:', err);
      });
  }, [id]);

  if (!crop) {
    return <div className="container mt-5">Loading...</div>;
  }

  return (
    <div className="container mt-5">
      <h1 className="mb-4">{crop.crop_name} - Companion Plants</h1>
      <Link to="/" className="btn btn-secondary mb-3">← Back to Crops</Link>
      <div className="row">
        {crop.companion_plants && crop.companion_plants.length > 0 ? (
          crop.companion_plants.map((plant, index) => (
            <div key={index} className="col-md-4 mb-4">
              <div className="card h-100">
                <img src={plant.image_url} className="card-img-top" alt={plant.name} />
                <div className="card-body">
                  <h5 className="card-title">{plant.name}</h5>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>No companion plants listed.</p>
        )}
      </div>
    </div>
  );
}

export default CompanionPlantPage;
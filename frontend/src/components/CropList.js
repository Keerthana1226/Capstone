import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function CropList() {
  const [crops, setCrops] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/crops')
      .then((res) => {
        setCrops(res.data);
      })
      .catch((err) => {
        console.error('Error fetching crops:', err);
      });
  }, []);

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Crop Companion App</h1>
      <div className="row">
        {crops.map((crop) => (
          <div key={crop._id} className="col-md-4 mb-4">
            <Link
              to={`/companions/${crop._id}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div className="card h-100">
                <img src={crop.crop_image_url} className="card-img-top" alt={crop.crop_name} />
                <div className="card-body">
                  <h5 className="card-title">{crop.crop_name}</h5>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CropList;
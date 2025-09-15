import React, { useState } from 'react';
import { Card, ListGroup } from 'react-bootstrap';

function CropCard({ crop }) {
  const [showCompanions, setShowCompanions] = useState(false);

  const handleCardClick = () => {
    setShowCompanions(!showCompanions);
  };

  return (
    <Card onClick={handleCardClick} style={{ cursor: 'pointer' }}>
      <Card.Img variant="top" src={crop.crop_image_url} />
      <Card.Body>
        <Card.Title>{crop.crop_name}</Card.Title>

        {showCompanions && (
          <>
            <Card.Subtitle className="mt-3 mb-2">Companion Plants:</Card.Subtitle>
            <ListGroup variant="flush">
              {crop.companion_plants.map((plant, index) => (
                <ListGroup.Item key={index}>
                  <img src={plant.image_url} alt={plant.name} style={{ width: '30px', marginRight: '10px' }} />
                  {plant.name}
                </ListGroup.Item>
              ))}
            </ListGroup>
          </>
        )}
      </Card.Body>
    </Card>
  );
}

export default CropCard;

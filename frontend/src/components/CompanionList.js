import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Container, Row, Col } from 'react-bootstrap';

function CompanionList({ cropName }) {
  const [companions, setCompanions] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:5000/api/crops/${cropName}/companions`)
      .then(res => setCompanions(res.data))
      .catch(err => console.log(err));
  }, [cropName]);

  return (
    <Container className="mt-4">
      <h2>Companion Plants for {cropName}</h2>
      <Row>
        {companions.map((comp, index) => (
          <Col md={3} key={index} className="mb-3">
            <Card>
              <Card.Img variant="top" src={comp.image_url} />
              <Card.Body>
                <Card.Title>{comp.name}</Card.Title>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default CompanionList;
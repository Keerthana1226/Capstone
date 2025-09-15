import React from 'react';
import DiseaseDetectionForm from '../components/DiseaseDetectionForm'; // Import the form component

function DiseaseDetectionPage() {
    return (
        <div className="page-container">
            <h1>🌿 Crop Disease Detection</h1>
            <p>Upload an image of a plant leaf to detect potential diseases.</p>
            <DiseaseDetectionForm />
        </div>
    );
}

export default DiseaseDetectionPage;
import React, { useState } from 'react';
// ⬇️ Import the new stylesheet ⬇️
import './DiseaseDetectionForm.css';

function DiseaseDetectionForm() {
    // State hooks...
    const [file, setFile] = useState(null);
    const [crop, setCrop] = useState('');
    const [prediction, setPrediction] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [imagePreview, setImagePreview] = useState('');
    // ⬇️ New state to track if a file is being dragged over the drop zone ⬇️
    const [isDragging, setIsDragging] = useState(false);

    // This function handles file selection from both the click-to-select and drag-and-drop
    const handleFileSelect = (selectedFile) => {
        if (selectedFile && selectedFile.type.startsWith('image/')) {
            setFile(selectedFile);
            setImagePreview(URL.createObjectURL(selectedFile));
            setError('');
        } else {
            setError('Please select a valid image file.');
        }
    };
    
    // --- Drag and Drop Event Handlers ---
    const handleDragOver = (event) => {
        event.preventDefault(); // This is necessary to allow a drop
        setIsDragging(true);
    };

    const handleDragLeave = (event) => {
        event.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        setIsDragging(false);
        const droppedFile = event.dataTransfer.files[0];
        handleFileSelect(droppedFile);
    };
    
    // Handles file selection when the file input is clicked
    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        handleFileSelect(selectedFile);
    };

    const handleCropChange = (event) => {
        setCrop(event.target.value);
    };

    // The submit logic with the corrected URL
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file || !crop) {
            setError('Please select a crop and upload an image.');
            return;
        }
        setIsLoading(true);
        setPrediction('');
        setError('');
        const formData = new FormData();
        formData.append('image', file);
        formData.append('crop', crop);
        try {
            // ✅ CORRECTED: Removed the trailing slash from the URL to prevent the 404 error.
            const response = await fetch('http://localhost:5000/api/disease-detection/detect', {
                method: 'POST',
                body: formData
                });

            if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
            
            const data = await response.json();
            if (data.prediction.includes('Error')) {
                setError(data.prediction);
            } else {
                setPrediction(data.prediction);
            }
        } catch (err) {
            console.error("Fetch error:", err);
            setError('An error occurred while making the prediction. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="detection-card">
            <form onSubmit={handleSubmit}>
                {/* Crop Selection */}
                <div className="mb-4">
                    <label htmlFor="crop-select" className="form-label fw-bold">1. Choose a Crop</label>
                    <select id="crop-select" className="form-select form-select-lg" value={crop} onChange={handleCropChange} required>
                        <option value="" disabled>Select your crop...</option>
                        <option value="maize">Maize</option>
                        <option value="rice">Rice</option>
                        <option value="wheat">Wheat</option>
                    </select>
                </div>

                {/* File Drop Zone */}
                <div className="mb-4">
                    <label className="form-label fw-bold">2. Upload an Image</label>
                    <div 
                        className={`file-drop-zone ${isDragging ? 'drag-over' : ''}`}
                        onDragOver={handleDragOver}
                        onDragLeave={handleDragLeave}
                        onDrop={handleDrop}
                        onClick={() => document.getElementById('image-upload').click()} // Trigger file input click
                    >
                        <input id="image-upload" type="file" accept="image/*" onChange={handleFileChange} />
                        <div className="upload-icon">
                            {/* Simple SVG Upload Icon */}
                            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" className="bi bi-cloud-arrow-up" viewBox="0 0 16 16"><path fillRule="evenodd" d="M7.646 5.146a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 6.707V10.5a.5.5 0 0 1-1 0V6.707L6.354 7.854a.5.5 0 1 1-.708-.708l2-2z"/><path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.785 2.23 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.825 10.328 3 8 3a4.53 4.53 0 0 0-2.941 1.1z"/></svg>
                        </div>
                        <p><strong>Drag & drop</strong> your image here, or click to select a file</p>
                    </div>
                </div>

                {/* Image Preview */}
                {imagePreview && (
                    <div className="image-preview">
                        <img src={imagePreview} alt="Selected crop" />
                    </div>
                )}
                
                {/* Submit Button */}
                <div className="d-grid mt-4">
                    <button type="submit" className="btn btn-primary btn-lg btn-submit" disabled={isLoading || !file || !crop}>
                        {isLoading ? (
                            <><span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...</>
                        ) : 'Detect Disease'}
                    </button>
                </div>
            </form>

            {/* Result Display */}
            <div className='mt-4'>
                {error && <div className="alert alert-danger">{error}</div>}
                {prediction && <div className="alert alert-success fs-5 text-center"><strong>Result:</strong> {prediction}</div>}
            </div>
        </div>
    );
}

export default DiseaseDetectionForm;
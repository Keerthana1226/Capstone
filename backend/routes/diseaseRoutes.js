// Import the express library to create our router.
const express = require('express');
// Create a new router object. This will handle all routes for this specific feature.
const router = express.Router();
// Import the multer library, which is essential for handling file uploads in Express.
const multer = require('multer');

// --- Import the Controller ---
// Intuition: We import the 'brain' of our operation. The controller contains the actual
// logic to run the Python script.
const diseaseController = require('../disease_detection/diseaseController');

// --- Configure Multer for File Storage ---
// Intuition: We need to tell the server where to temporarily save the uploaded images
// before they are processed.
const storage = multer.diskStorage({
  // 'destination' tells multer which folder to save the files in.
  destination: function (req, file, cb) {
    // We save them in an 'uploads' folder. 'cb' is a callback function to continue.
    cb(null, 'uploads/'); 
  },
  // 'filename' tells multer how to name the file to avoid conflicts.
  filename: function (req, file, cb) {
    // We create a unique name by adding the current timestamp to the original filename.
    cb(null, Date.now() + '-' + file.originalname);
  }
});

// Initialize multer with our storage configuration.
const upload = multer({ storage: storage });

// --- Define the API Route ---
// Intuition: This is the most important part. We are creating the specific "instruction"
// for the '/detect' path that was previously missing.
router.post( // We specify this route handles POST requests.
    '/detect', // The path for this route. The full URL will be /api/disease-detection/detect.
    upload.single('image'), // This is middleware. It tells multer to look for a single file named 'image' and process it first.
    diseaseController.detectDisease // After the file is uploaded, run our main logic from the controller.
);


// Export the fully configured router so server.js can use it.
module.exports = router;
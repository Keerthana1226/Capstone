const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

// POST route to predict crop
router.post('/', (req, res) => {
    console.log('📥 Received POST to /api/crop-recommend');
    console.log('🧪 Request Body:', req.body);

    const {
        nitrogen,
        phosphorus,
        potassium,
        temperature,
        humidity,
        ph,
        rainfall
    } = req.body;

    const scriptPath = path.join(__dirname, '..', 'crop_recommendation', 'crop_predictor.py');
    console.log('🔍 Python Script Path:', scriptPath);

    const pythonProcess = spawn('python', [
        scriptPath,
        nitrogen,
        phosphorus,
        potassium,
        temperature,
        humidity,
        ph,
        rainfall
    ]);

    let result = '';

    pythonProcess.stdout.on('data', (data) => {
        console.log('📤 Python stdout:', data.toString());
        result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error('❌ Python stderr:', data.toString());
    });

    pythonProcess.on('close', (code) => {
        console.log('✅ Python script exited with code:', code);
        if (code !== 0) {
            return res.status(500).json({ error: 'Error occurred while predicting crop' });
        }

        const prediction = result.trim();
        console.log('🌱 Predicted Crop:', prediction);

        res.json({ predicted_crop: prediction });
    });
});

module.exports = router;
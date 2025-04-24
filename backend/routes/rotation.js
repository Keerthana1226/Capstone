// backend/routes/rotation.js
const express = require('express');
const router = express.Router();
const controller = require('../rotation/controller');

// POST route to run crop recommendation
router.post('/run-recommendation', controller.runCropRecommendation);

module.exports = router;

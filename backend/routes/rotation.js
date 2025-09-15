const express = require('express');
const router = express.Router();
const { runCropRecommendation } = require('../rotation/controller');

router.post('/run-recommendation', runCropRecommendation);

module.exports = router;
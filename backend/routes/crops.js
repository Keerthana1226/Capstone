const express = require('express');
const router = express.Router();
const Crop = require('../models/Crop'); // Correct import path

// GET all crops
router.get('/', async (req, res) => {
  try {
    const crops = await Crop.find();
    res.json(crops);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// GET specific crop by ID (for companion plant page)
router.get('/:id', async (req, res) => {
  try {
    const crop = await Crop.findById(req.params.id);
    if (!crop) {
      return res.status(404).json({ message: 'Crop not found' });
    }
    res.json(crop);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
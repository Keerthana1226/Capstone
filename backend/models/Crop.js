const mongoose = require('mongoose');

const CropSchema = new mongoose.Schema({
  crop_name: String,
  crop_image_url: String,
  companion_plants: [
    {
      name: String,
      image_url: String,
    },
  ],
});

module.exports = mongoose.model('Crop', CropSchema, 'companionPlants');
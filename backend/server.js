const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

// --- EXISTING ROUTES ---
const cropRoutes = require('./routes/crops');
const rotationRoutes = require('./routes/rotation');
const cropRecommendRoute = require('./routes/cropRecommend');
// --- ⬇️ 1. IMPORT NEW DISEASE ROUTE ⬇️ ---
const diseaseRoutes = require('./routes/diseaseRoutes'); // Imports the new route handlers

const app = express();

app.use(cors());
app.use(express.json());

// MongoDB Connection (no changes here)
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('✅ MongoDB connected successfully'))
  .catch(err => console.error('❌ MongoDB connection failed:', err));

// --- EXISTING ROUTES ---
app.use('/api/crops', cropRoutes);
app.use('/api/rotation-plan', rotationRoutes);
app.use('/api/crop-recommend', cropRecommendRoute);
// --- ⬇️ 2. MOUNT NEW DISEASE ROUTE ⬇️ ---
app.use('/api/disease-detection', diseaseRoutes); // Tells the app to use diseaseRoutes for any URL starting with /api/disease

// Root Route (no changes here)
app.get('/', (req, res) => {
  res.send('Crop Companion API is running...');
});

// Server Listen (no changes here)
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server started on port ${PORT}`));
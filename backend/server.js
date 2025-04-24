const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const cropRoutes = require('./routes/crops');
const rotationRoutes = require('./routes/rotation');
const cropRecommendRoute = require('./routes/cropRecommend');

const app = express();

app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('✅ MongoDB connected successfully'))
  .catch(err => console.error('❌ MongoDB connection failed:', err));

// Routes
app.use('/api/crops', cropRoutes);

app.use('/api/rotation-plan', rotationRoutes);


// Root Route
app.get('/', (req, res) => {
  res.send('Crop Companion API is running...');
});


// Mount the route
app.use('/api/crop-recommend', cropRecommendRoute);


// Server Listen
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server started on port ${PORT}`));

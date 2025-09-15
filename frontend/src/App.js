import { Routes, Route} from 'react-router-dom';
import CompanionPlantPage from './pages/CompanionPlantPage';
import CropRotationPage from './pages/CropRotationPage';
import CropRecommendation from './components/CropRecommendation';
import CropList from './components/CropList'
import 'bootstrap/dist/css/bootstrap.min.css';
import HomePage from './pages/HomePage';
import DiseaseDetectionPage from './pages/DiseaseDetectionPage';


function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path='/crops' element={<CropList />} />
      <Route path="/companions/:id" element={<CompanionPlantPage />} />
      <Route path="/rotation" element={<CropRotationPage />} />
      <Route path="/crop-recommend" element={<CropRecommendation />} />
      <Route path="/disease-detection" element={<DiseaseDetectionPage />} />
    </Routes>
  );
}

export default App;
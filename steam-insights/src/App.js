import React from 'react';
import GenreChart from './components/GenreCountChart';
import AvgReviewChart from './components/avgReviewChart';
import PeakUserChart from './components/PeakUserChart'; 
import TopGamesChart from './components/TopGamesChart';
import PredictionForm from './components/PredictionForm';
import './Formats.css'; 

function App() {
  return (
    <div className="dashboard">
      {/*top row*/}
      <div className="chart-row">
        <div className="chart">
          <GenreChart />
        </div>
      </div>
      {/*bottom row*/}
      <div className="chart-row">
        <div className="chart">
          <AvgReviewChart />
        </div>
        <div className="chart">
          <PeakUserChart />
        </div>
      </div>
      <div className="chart-row">
        <div className="chart">
          <TopGamesChart />
        </div>
      </div>
      <div className="chart-row">
        <div className="chart">
          <PredictionForm />
        </div>
      </div>
    </div>
  );
}

export default App;

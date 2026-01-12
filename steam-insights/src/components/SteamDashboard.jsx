import React from 'react';
import GenreChart from '../components/UI/GenreCountChart';
import AvgReviewChart from '../components/UI/avgReviewChart';
import PeakUserChart from '../components/UI/PeakUserChart'; 
import TopGamesChart from '../components/UI/TopGamesChart';
import PredictionForm from '../components/UI/PredictionForm';
import '../Formats.css'; 

function App() {
  return (
    <div className="dashboard">
      {/*top row*/}
      <div className="description">
        <h1>Steam Indie Game Insights</h1>
      </div>
      <div className="chart-row">
        <div className="chart">
          <TopGamesChart />
        </div>
      </div>
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
          <PredictionForm />
        </div>
      </div>
    </div>
  );
}

export default App;

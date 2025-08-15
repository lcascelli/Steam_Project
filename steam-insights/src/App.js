import React from 'react';
import GenreChart from './components/GenreCountChart';
import AvgReviewChart from './components/avgReviewChart';
import PeakUserChart from './components/PeakUserChart'; 
import './Formats.css'; 

function App() {
  return (
    <div className="dashboard">
      {/*top row*/}
      <div className="chart-row">
        <div className="chart">
          <GenreChart />
        </div>
        <div className="chart">
          <AvgReviewChart />
        </div>
      </div>
      {/*bottom row*/}
      <div className="chart-row">
        <div className="chart">
          <PeakUserChart />
        </div>
        <div className="chart">
          <h2>Additional Charts Coming Soon!</h2>
          <p>Stay tuned for more insights and visualizations.</p>
        </div>
      </div>
    </div>
  );
}

export default App;

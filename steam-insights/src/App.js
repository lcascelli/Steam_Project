import React from 'react';
import GenreChart from './components/UI/GenreCountChart';
import AvgReviewChart from './components/UI/avgReviewChart';
import PeakUserChart from './components/UI/PeakUserChart'; 
import TopGamesChart from './components/UI/TopGamesChart';
import PredictionForm from './components/UI/PredictionForm';
import './Formats.css'; 

function App() {
  return (
    <div className="dashboard">
      {/*top row*/}
      <div className="description">
        <h1>Steam Indie Game Insights</h1>
        <p>
          Steam Indie Game Insights is a data-driven web application that analyzes
          trends in indie game performance on Steam. The project uses a Python-based
          data pipeline to collect and process SteamSpy data, stores curated datasets
          in Google BigQuery, and serves machine learning predictions through a FastAPI
          backend. The frontend is built with React and interactive visualizations to
          explore genre trends, player engagement, review sentiment, and top-performing
          games. The prediction tool at the bottom allows users to simulate how different game
          attributes may impact ownership outcomes, showcasing an end-to-end workflow
          from data ingestion and modeling to production deployment. Please note that the 
          the prediction tool will take a minute to load on the first try.
        </p>
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

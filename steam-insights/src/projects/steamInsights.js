import App from "../components/SteamDashboard";

export const steamInsights = {
    id: 'steam-insights',
    title: 'Market Analysis Dashboard and ML Prediction Tool for Indie Games on Steam',
    description: `Steam Indie Game Insights is a data-driven web application that analyzes
              trends in indie game performance on Steam. The project uses a Python-based
              data pipeline to collect and process SteamSpy data, stores curated datasets
              in Google BigQuery, and serves machine learning predictions through a FastAPI
              backend. The frontend is built with React and interactive visualizations to
              explore genre trends, player engagement, review sentiment, and top-performing
              games. The prediction tool at the bottom allows users to simulate how different game
              attributes may impact ownership outcomes, showcasing an end-to-end workflow
              from data ingestion and modeling to production deployment. Please note that the 
              the prediction tool will take a minute to load on the first try.`,
    techstack: ["Python", 
    "React",
    "scikit-learn",
    "Google Cloud Platform",
    "FastAPI",
    "SteamSpy API",
    "pandas"
    ],
    type: 'react',
    component: < App />,
    repo: 'https://github.com/lcascelli/Steam_Project'
}
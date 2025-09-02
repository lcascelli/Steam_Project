import React, {useEffect, useState} from "react";
import { getPrediction } from "../services/api_pull";
import avg_by_genre from "../data/avg_by_genre.json";

function PredictionForm() {
    const [selectedGenre, setSelectedGenre] = useState([]);
    const [inputData, setInputData] = useState({});
    const [Result, setResult] = useState(null);

    //extracting genre names
    const genresLookup = avg_by_genre.reduce((acc, g) => {
        acc[g.genre.toLowerCase()] = g;
        return acc;
    }, {});
    const genres = Object.keys(genresLookup);


    useEffect(() => {
        if (selectedGenre.length === 0) return;
        
        let sums = { positive: 0, negative: 0, avg_forever: 0, median_forever: 0, ccu: 0};
        selectedGenre.forEach((genre) => {
            const g = avg_by_genre[genre];
            sums.positive += g.avg_positive;
            sums.negative += g.avg_negative;
            sums.avg_forever += g.avg_forever;
            sums.median_forever += g.avg_forever; // Use avg_forever as a proxy for median_forever
            sums.ccu += g.avg_2week; // Use avg_2week as a proxy for ccu
        });

        const count = selectedGenre.length;
        const averages = {
            positive: Math.round(sums.positive / count),
            negative: Math.round(sums.negative / count),
            avg_forever: Math.round(sums.avg_forever / count),
            median_forever: Math.round(sums.median_forever / count),
            ccu: Math.round(sums.ccu / count),
        };

        const newInputData = {
            ...Object.fromEntries(genres.map(g => [g, selectedGenre.includes(g) ? 1 : 0])),
            ...averages,
            same_dev_pub: 1,
        };

        setInputData(newInputData);
    }, [selectedGenre]);

    const handleGenreChange = (e) => {
        const { value, checked } = e.target;
        setSelectedGenre(prev => 
            checked ? [...prev, value] : prev.filter(g => g !== value)
        );
    };

    const handlePredict = async () => {
        try {
            const prediction = await getPrediction(inputData);
            setResult(prediction);
        } catch (error) {
            console.error("Error fetching prediction:", error);
        }
    };

    return (
        <div>
            <h2>ML Prediction</h2>

            <div style={{display: "flex", flexWrap: "wrape", gap: "10px"}}>
                {genres.map((genre) => (
                    <label key={genre} style={{marginRight: "10px"}}>
                        <input
                            type="checkbox"
                            value={genre}
                            checked={selectedGenre.includes(genre)}
                            onChange={handleGenreChange}
                        />
                        {genre}
                    </label>
                ))}
            </div>
            <button onClick={handlePredict} style={{marginTop: "10px"}}>
                Get Predict
            </button>

            <pre style={{background: "#f4f4f4", padding: "10px"}}>
                {JSON.stringify(inputData, null, 2)}
            </pre>
            {Result && (
                <div>
                    <h3>Prediction Result:</h3>
                    <pre> {JSON.stringify(Result, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default PredictionForm;

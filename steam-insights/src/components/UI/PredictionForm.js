import React, {useEffect, useState} from "react";
import { getPrediction } from "../../services/api_pull";
import avg_by_genre from "../../data/avg_by_genre.json";


const displayNames = {
    //Action: "Action",
    //Casual: "Casual",
    //Adventure: "Adventure",
    //Simulation: "Simulation",
    //Strategy: "Strategy",
    //RPG: "RPG",
    //Early_Access: "Early Access",
    //Free_To_Play: "Free to Play",
    //Sports: "Sports",
    //Racing: "Racing",
    //Massively_Multiplayer: "Massive Multiplayer",
    //Violent: "Violent",
    //Gore: "Gore",
    positive: "Positive Reviews",
    negative: "Negative Reviews",
    average_forever: "Average Number of Users",
    median_forever: "Median Number of Users",
    ccu: "Concurrent Users (Snapshot)",
    same_dev_pub: "Same Developer and Publisher",
};

const featureKeys = [
    "positive",
    "negative",
    "average_forever",
    "median_forever",
    "ccu",
    "same_dev_pub",
];

function PredictionForm() {
    const [selectedGenre, setSelectedGenre] = useState([]);
    const [inputData, setInputData] = useState({});
    const [Result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const genres = React.useMemo(() => Object.keys(avg_by_genre), []);

    useEffect(() => {
        if (selectedGenre.length === 0) return;
        

        //using some proxies for values that I have. 
        //***FIXME: bigquery for avg_by_genre.json to get median_forever and ccu averages for each genre***


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
            Action: selectedGenre.includes("action") ? 1 : 0,
            Casual: selectedGenre.includes("casual") ? 1 : 0,
            Adventure: selectedGenre.includes("adventure") ? 1 : 0,
            Simulation: selectedGenre.includes("simulation") ? 1 : 0,
            Strategy: selectedGenre.includes("strat") ? 1 : 0,
            RPG: selectedGenre.includes("rpg") ? 1 : 0,
            Early_Access: selectedGenre.includes("early") ? 1 : 0,
            Free_To_Play: selectedGenre.includes("free") ? 1 : 0,
            Sports: selectedGenre.includes("sport") ? 1 : 0,
            Racing: selectedGenre.includes("racing") ? 1 : 0,
            Massively_Multiplayer: selectedGenre.includes("mmo") ? 1 : 0,
            Violent: selectedGenre.includes("violent") ? 1 : 0,
            Gore: selectedGenre.includes("gore") ? 1 : 0,
            positive: averages.positive,
            negative: averages.negative,
            average_forever: averages.avg_forever,
            median_forever: averages.median_forever,
            ccu: averages.ccu,
            same_dev_pub: 1,
        };



        if (JSON.stringify(newInputData) !== JSON.stringify(inputData)) {
            setInputData(newInputData);
        }
    }, [selectedGenre, genres, inputData]);

    const handleGenreChange = (e) => {
        const { value, checked } = e.target;
        const val = value.toLowerCase();
        setSelectedGenre(prev => 
            checked ? [...prev, val] : prev.filter(g => g !== val)
        );
    };

    const handleInputChange = (e, key) => {
        let value = e.target.value;
        if (key !== "same_dev_pub") {
            value = Number(value);
        } else {
            value = value === "1" ? 1 : 0;
        }    
        setInputData(prev => ({ ...prev, [key]: value }));
    };

    const handlePredict = async () => {
        console.log("Sending inputData:", inputData);
        setLoading(true);
        try {
            const prediction = await getPrediction(inputData);
            console.log("Prediction Results:", prediction);
            setResult(prediction);
        } catch (error) {
            console.error("Error fetching prediction:", error);
        } finally {
            setLoading(false);
        }

    }

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
                        {genre.charAt(0).toUpperCase() + genre.slice(1)}
                    </label>
                ))}
            </div>
            <form style={{marginTop: "20px", display: "flex", flexWrap: "wrap", gap: "10px"}}>
                {featureKeys.map((key) => (
                    <div key={key} style={{marginRight: "20px"}}>
                        <label>
                            {displayNames[key] || key}:
                            {key === "same_dev_pub" ? (
                                <select
                                    value={inputData[key] ?? 1}
                                    onChange={(e) => handleInputChange(e, key)}
                                    style={{marginLeft: "10px"}}
                                >
                                    <option value={1}>Yes</option>
                                    <option value={0}>No</option>
                                </select>
                            ) : (
                                <input
                                    type="number"
                                    value={inputData[key] ?? ""}
                                    onChange={(e) => handleInputChange(e, key)}
                                    style={{marginLeft: "10px", width: "100px"}}
                                />
                            )}
                        </label>
                    </div>
                ))}
            </form>
            <button onClick={handlePredict} disable={loading} style={{marginTop: "10px"}}>
                {loading ? "Waiting for backend, this may take up to a minute for the backend API to wake up..." : "Predict"}
                Get Predict
            </button>
            <h3 style={{marginTop: "50px"}}>Input Values</h3>
            <div style={{marginTop: "10px", display: "flex", gap: "40px", alignItems: "flex-start"}}>
                
                <table style={{borderCollapse: "collapse", minWidth: "500px"}}>
                    <thead>
                            <tr>
                                <th style={{border: "1px solid #ddd", padding:"8px"}}>Feature</th>
                                <th style={{border: "1px solid #ddd", padding:"8px"}}>Value</th>
                            </tr>
                    </thead>
                    <tbody>
                        {featureKeys.map(key => (
                            <tr key={key}>
                                <td style={{border: "1px solid #ddd", padding:"8px"}}>{displayNames[key]}</td>
                                <td style={{border: "1px solid #ddd", padding:"8px"}}>{inputData[key]}</td>
                            </tr>
                            ))}
                    </tbody>
                </table>
                {Result && (
                <div style = {{padding: "16px", borderRadius: "8px", minWidth: "300px"}}>
                    <h3 style={{marginTop: "-70px"}}>Prediction Result:</h3>
                    <div style={{fontSize: "1.1em", fontWeight:"bold", marginBottom:"10px"}}>
                        Predicted Ownership Range: 
                    </div>
                    <div style={{fontSize:"1em", padding: "8px"}}>
                        {Result["Predicted Ownership Range"]}
                    </div>
                    <div style={{fontSize: "1.1em", fontWeight:"bold"}}>
                        Predicted Probabilities Across Classes:
                    </div>
                    <div style={{fontFamily:"monospace", fontSize:"1em", padding: "8px"}}>
                        {Result["Predicted Probabilities Across Classes"] &&
                            Object.entries(Result["Predicted Probabilities Across Classes"]).map(([range, prob]) => (
                                <div key={range}>
                                    {range}: {prob}
                                </div>
                            ))}
                    </div>
                </div>
            )}
            </div>
        </div>
    );
}

export default PredictionForm;


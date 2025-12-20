import React, { /*useEffect,*/ useMemo, useState } from 'react';
import genreData from '../data/df_indie_simple.json';
import { genreLabels } from '../components/genreLabels.js';


function TopGamesChart() {
    const [SelectedGenres, setSelectedGenres] = useState([]);

    const preprocessedGames = useMemo(() => {
        return genreData.map(game => ({
            ...game,
            genres_list: game.genres_list || []
        }));
    }, []);

    const genres = Object.values(genreLabels);
    
    /* This is the old version with all genres in list. Line above is curated genre list
    Array.from(
        new Set(genreData.flatMap(game => game.genres_list || []))
    ).sort();

    */ 

    const filteredGames = useMemo(() => {
        let filtered = preprocessedGames;

        if (SelectedGenres.length > 0) {
            filtered = filtered.filter(game =>
                SelectedGenres.every(genre => game.genres_list.includes(genre))
            );
        }
        return filtered
            .sort((a, b) => b.owners_lower - a.owners_lower)
            .slice(0, 10);
    }, [SelectedGenres, preprocessedGames]);

console.log(genreData.flatMap(game => game.genres_list));

/* 

This still needs to be fixed. Right now it is a small scrollable box, but I want to be able to have a multi-select feature

    useEffect(() => {
        let filtered = genreData;
        if (SelectedGenres.length > 0) {
            filtered = genreData.filter(game =>
                SelectedGenres.every(genre => game.genres_list.includes(genre))
            );
        }

        const topGames = filtered
        .sort((a, b) => b.owners_lower - a.owners_lower)
        .slice(0, 10);

        setFilteredGames(topGames);
    }, [SelectedGenres]);

    */

const handleGenreChange = (e) => {
    const { value, checked } = e.target;
    setSelectedGenres(prev =>
        checked ? [...prev, value] : prev.filter(genre => genre !== value)
    );
};

    return (
        <div>
            <h2>Top 10 Games By Ownership</h2>
            {/*filter logic*/}
            <div style= {{ 
                display: "flex", 
                flexWrap: "wrap", 
                gap: "10px",
                marginBottom: "15px" 
                }}
            >
                {genres && genres.length > 0 ? (
                genres.map(({ label, value}) => (
                    <label key={value} style={{marginRight: "10px"}}>
                        <input
                            type="checkbox"
                            value={value}
                            checked={SelectedGenres.includes(genre)}
                            onChange={handleGenreChange}
                        />
                        {label}
                    </label>
                ))
            ) : (
                <p>Loading genres...</p>
            )}
            </div>
            {/*chart*/}
            <table border="1" cellPadding="5" style={{ marginTop: "10px", width: "100%" }}>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Ownership Range</th>
                        <th>Genres</th>
                        <th>Peak Users</th>
                        <th>Positive Reviews</th>
                        <th>Negative Reviews</th>
                        <th>Publisher</th>
                        <th>Developer</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredGames.map((game) => (
                        <tr key={game.appid}>
                            <td>{game.name}</td>
                            <td>{game.owners.toLocaleString()}</td>
                            <td>{(game.genres_list || []).join(', ')}</td>
                            <td>{game.average_forever.toLocaleString()}</td>
                            <td>{game.positive.toLocaleString()}</td>
                            <td>{game.negative.toLocaleString()}</td>
                            <td>{game.publisher}</td>
                            <td>{game.developer}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
export default TopGamesChart;
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import genreData from '../data/df_indie_simple.json';

function TopGamesChart() {
    const [SelectedGenres, setSelectedGenres] = useState([]);
    const [filteredGames, setFilteredGames] = useState([]);

    const genres = Array.from(
        new Set(genreData.flatMap(game => game.genre_list))
    );

    useEffect(() => {
        let filtered = genreData;
        if (SelectedGenres.length > 0) {
            filtered = genreData.filter(game =>
                SelectedGenres.some(genre => game.genre_list.includes(genre))
            );
        }

        const topGames = filtered
        .sort((a, b) => b.owners_lower - a.owners_lower)
        .slice(0, 10);

        setFilteredGames(topGames);
    }, [SelectedGenres]);

    return (
        <div>
            <h2>Top 10 Games By Ownership</h2>
            {/*filter logic*/}
            <select
                multiple
                value={SelectedGenres}
                onChange={(e) =>
                    setSelectedGenres(
                        Array.from(e.target.selectedOptions, option => option.value)
                    )
                }
            >
                {genres.map((genre) => (
                    <option key={genre} value={genre}>
                        {genre}
                    </option>
                ))}
            </select>
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
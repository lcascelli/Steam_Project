import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import genreData from '../data/avg_by_genre.json';
import { genreLabels } from '../components/genreLabels';


const sortedData = Object.entries(genreData)
        .map(([genre, data]) => ({
            ...data,
            genre,
            genre_count: Number(data.genre_count),
        }))
        .sort((a, b) => a.genre_count - b.genre_count)
        .reverse()
        .map(d => ({
                ...d,
                genreLabel: genreLabels[d.genre] || d.genre
                  }));

const GenreChart = () => {
    return (
        <div style={{ width: '80%', height: 600 }}>
        <h2> Count of Games by Top Genres </h2>
        <ResponsiveContainer>
            <BarChart data={sortedData} layout="vertical" margin={{ top: 20, right: 30, left: 100, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number"/>
                <YAxis dataKey="genreLabel" type = "category"/>
                <Tooltip />
                <Legend verticalAlign='top' align ="right"/>
                <Bar dataKey="genre_count" fill="#8884d8" name="Game Count"/>
            </BarChart>
        </ResponsiveContainer>
        </div>
    );
}
export default GenreChart;
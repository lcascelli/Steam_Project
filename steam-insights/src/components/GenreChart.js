import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import genre_agg from '../data/genres_agg.json';

const labelMap = {
  sum_action: 'Action',
  sum_adventure: 'Adventure',
  sum_rpg: 'RPG',
  sum_mmo: 'MMO',
  sum_violent: 'Violent',
  sum_gore: 'Gore',
  sum_strat: 'Strategy',
  sum_racing: 'Racing',
  sum_sim: 'Simulation',
  sum_casual: 'Casual',
  sum_early: 'Early Access',
  sum_free: 'Free to Play',
  sum_sport: 'Sports',
};


const data = Object.entries(genre_agg).map(([key, value]) => ({
    genre: labelMap[key] || key,
    count: value,
}))
.sort((a, b) => b.count - a.count);

const GenreChart = () => {
    return (
        <div style={{ width: '80%', height: 700 }}>
        <h2> Count of Games by Top Genres </h2>
        <ResponsiveContainer>
            <BarChart data={data} layout="vertical" margin={{ top: 20, right: 30, left: 100, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="genre" type = "category"/>
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
        </ResponsiveContainer>
        </div>
    );
}
export default GenreChart;
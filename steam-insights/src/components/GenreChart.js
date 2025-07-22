import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import data from './df_games.json';

console.log("Chart data:", data);
// Ensure the data is in the expected format

const GenreChart = () => {
    return (
        <div style={{ width: '100%', height: 300 }}>
        <h2> Average Positive Reviews by Genre </h2>
        <ResponsiveContainer>
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="genre" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
        </ResponsiveContainer>
        </div>
    );
}
export default GenreChart;
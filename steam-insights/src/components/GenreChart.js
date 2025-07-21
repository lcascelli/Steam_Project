import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
    { genre: 'Action', count: 4000 },
    { genre: 'Adventure', count: 3000 },
    { genre: 'RPG', count: 2000 },
    { genre: 'Simulation', count: 2780 },
    { genre: 'Strategy', count: 1890 },
    { genre: 'Casual', count: 2390 },
]

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
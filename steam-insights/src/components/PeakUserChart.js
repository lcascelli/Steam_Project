import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import genreData from '../data/avg_by_genre.json';
import { genreLabels } from '../components/genreLabels';


const sortedData = Object.entries(genreData)
        .map(([genre, data]) => ({
            ...data,
            genre,
            avg_forever: Number(data.avg_forever),
        }))
        .sort((a, b) => a.avg_forever - b.avg_forever)
        .reverse()
        .map(d => ({
                ...d,
                genreLabel: genreLabels[d.genre]?.label || d.genre
                  }));


const PeakUserChart = () => {
    return (
        <div style={{ width: '80%', height: 600 }}>
        <h2> Average Peak Users by Top Genres </h2>
        <ResponsiveContainer>
            <BarChart data={sortedData} layout="vertical" margin={{ top: 20, right: 30, left: 100, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number"/>
                <YAxis dataKey="genreLabel" type = "category"/>
                <Tooltip />
                <Legend verticalAlign='top' align ="center"/>
                <Bar dataKey="avg_forever" fill="#8884d8" name="Peak Users"/>
            </BarChart>
        </ResponsiveContainer>
        </div>
    );
}
export default PeakUserChart;
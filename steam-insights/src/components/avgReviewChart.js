import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import genreData from '../data/avg_by_genre.json';
import { genreLabels } from '../components/genreLabels';

const sortedData = [...genreData]
        .map(d => ({...d, avg_positive: Number(d.avg_positive) }))
        .sort((a, b) => a.avg_positive - b.avg_positive)
        .reverse()
        .map(d => ({
                ...d,
                genreLabel: genreLabels[d.genre] || d.genre
                  }));

const AvgReviewChart = () => {
        return (
            <div style={{ width: '80%', height: 600 }}>
            <h2> Average Reviews of Top Genres </h2>
            <ResponsiveContainer>
                <BarChart data={sortedData} layout="vertical" margin={{ top: 20, right: 30, left: 100, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number"/>
                    <YAxis dataKey="genreLabel" type = "category"/>
                    <Tooltip />
                    <Legend verticalAlign="top" align= 'right' />
                    <Bar dataKey="avg_positive" stackId="reviews" fill="#209708ff" name="Average Positive Reviews"/>
                    <Bar dataKey="avg_negative" stackId="reviews" fill="#e21e1eff" name="Average Negative Reviews"/>
                </BarChart>
            </ResponsiveContainer>
            </div>
        );
    }
    export default AvgReviewChart;
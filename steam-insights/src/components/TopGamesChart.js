import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import genreData from '../data/df_indie.json';

const metricOptions = [
    { value: "average_forever", label: "Average Playtime (Forever_" },
]
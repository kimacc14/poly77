"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';

interface SentimentData {
  timestamp: string;
  sentiment_score: number;
  mention_count: number;
}

export default function SentimentChart({ data }: { data: SentimentData[] }) {
  const chartData = data.map(d => ({
    time: format(new Date(d.timestamp), 'HH:mm'),
    sentiment: d.sentiment_score,
    mentions: d.mention_count
  }));

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Trend</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis yAxisId="left" domain={[-1, 1]} />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="sentiment"
            stroke="#0ea5e9"
            strokeWidth={2}
            name="Sentiment Score"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="mentions"
            stroke="#10b981"
            strokeWidth={2}
            name="Mentions"
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 bg-primary-600"></div>
          <span className="text-gray-600">Sentiment Score</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 bg-success"></div>
          <span className="text-gray-600">Mention Count</span>
        </div>
      </div>
    </div>
  );
}

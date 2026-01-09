import { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Market {
  id: number;
  platform: string;
  market_id: string;
  title: string;
  description: string;
  category: string;
  current_probability: number;
  volume: number;
  close_time: string;
}

interface Prediction {
  predicted_shift: number;
  confidence_level: string;
  reasoning: string;
  time_horizon: string;
}

export default function MarketCard({ market }: { market: Market }) {
  const [expanded, setExpanded] = useState(false);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);

  const loadPrediction = async () => {
    if (!expanded && !prediction) {
      setLoading(true);
      try {
        const response = await axios.get(`${API_BASE_URL}/api/markets/${market.id}`);
        if (response.data.predictions && response.data.predictions.length > 0) {
          setPrediction(response.data.predictions[0]);
        }
      } catch (error) {
        console.error('Error loading prediction:', error);
      }
      setLoading(false);
    }
    setExpanded(!expanded);
  };

  const getTradeUrl = () => {
    if (market.platform === 'kalshi') {
      return `https://kalshi.com/markets/${market.market_id}`;
    } else if (market.platform === 'polymarket') {
      return `https://polymarket.com/`;
    }
    return '#';
  };

  const getProbabilityColor = (prob: number) => {
    if (prob >= 0.7) return 'text-green-600';
    if (prob >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceColor = (level: string) => {
    if (level === 'high') return 'bg-green-100 text-green-800';
    if (level === 'medium') return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
      {/* Header */}
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <span className={`px-3 py-1 rounded-full text-xs font-medium uppercase ${
            market.platform === 'kalshi' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'
          }`}>
            {market.platform}
          </span>
          <span className="text-xs text-gray-500 capitalize">{market.category}</span>
        </div>

        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          {market.title}
        </h3>

        {/* Probability */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm text-gray-600">Current Probability</span>
            <span className={`text-2xl font-bold ${getProbabilityColor(market.current_probability)}`}>
              {(market.current_probability * 100).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all"
              style={{ width: `${market.current_probability * 100}%` }}
            />
          </div>
        </div>

        {/* Volume */}
        <div className="text-sm text-gray-600 mb-4">
          Volume: ${market.volume.toLocaleString()}
        </div>

        {/* Buttons */}
        <div className="flex gap-2">
          <button
            onClick={loadPrediction}
            className="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg font-medium transition-colors"
          >
            {expanded ? 'Hide Details' : 'View Details'}
          </button>
          <a
            href={getTradeUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors text-center"
          >
            Trade Now
          </a>
        </div>
      </div>

      {/* Expanded Details */}
      {expanded && (
        <div className="border-t border-gray-200 p-6 bg-gray-50">
          {loading ? (
            <div className="text-center py-4">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : prediction ? (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">AI Prediction</h4>

              <div className="space-y-3">
                {/* Predicted Shift */}
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Predicted Shift ({prediction.time_horizon})</span>
                  <span className={`text-lg font-bold ${
                    prediction.predicted_shift > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {prediction.predicted_shift > 0 ? '+' : ''}{prediction.predicted_shift.toFixed(2)}%
                  </span>
                </div>

                {/* Confidence */}
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Confidence</span>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium uppercase ${
                    getConfidenceColor(prediction.confidence_level)
                  }`}>
                    {prediction.confidence_level}
                  </span>
                </div>

                {/* Reasoning */}
                <div className="mt-4 p-3 bg-white rounded-lg border border-gray-200">
                  <p className="text-sm text-gray-700">{prediction.reasoning}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-4 text-gray-600">
              <p>No prediction data available</p>
            </div>
          )}

          {/* Description */}
          {market.description && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-700">{market.description}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

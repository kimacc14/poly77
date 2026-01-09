"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';
import MarketCard from '@/components/MarketCard';
import SentimentChart from '@/components/SentimentChart';
import AlertPanel from '@/components/AlertPanel';

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

interface Alert {
  id: number;
  alert_type: string;
  topic: string;
  message: string;
  severity: string;
  created_at: string;
  read: boolean;
}

export default function Home() {
  const [markets, setMarkets] = useState<Market[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    fetchMarkets();
    fetchAlerts();

    // Set up WebSocket connection
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'market_update') {
        fetchMarkets();
      } else if (data.type === 'alert') {
        fetchAlerts();
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  const fetchMarkets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/markets`, {
        params: { limit: 50 }
      });
      setMarkets(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching markets:', error);
      setLoading(false);
    }
  };

  const fetchAlerts = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/alerts`, {
        params: { limit: 10 }
      });
      setAlerts(response.data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const filteredMarkets = selectedCategory === 'all'
    ? markets
    : markets.filter(m => m.category === selectedCategory);

  const categories = Array.from(new Set(markets.map(m => m.category)));

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            AI-Powered Mindshare Market Analyzer
          </h1>
          <p className="mt-2 text-gray-600">
            Real-time sentiment analysis and prediction market insights
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alert Panel */}
        <div className="mb-8">
          <AlertPanel alerts={alerts} />
        </div>

        {/* Category Filter */}
        <div className="mb-6">
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedCategory === 'all'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              All Markets
            </button>
            {categories.map(category => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors capitalize ${
                  selectedCategory === category
                    ? 'bg-primary-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Markets Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="mt-4 text-gray-600">Loading markets...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredMarkets.map(market => (
              <MarketCard key={market.id} market={market} />
            ))}
          </div>
        )}

        {!loading && filteredMarkets.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-600">No markets found for this category</p>
          </div>
        )}
      </div>
    </main>
  );
}

export type Platform = 'polymarket' | 'kalshi';

export interface Market {
  id: number;
  platform: Platform | string;
  market_id: string;
  title: string;
  description: string;
  category: string;
  current_probability: number;
  volume: number;
  close_time: string;
  collateral_currency?: 'pUSD' | 'USD';
}

import { describe, expect, it } from 'vitest';
import {
  POLYMARKET_API_ENDPOINTS,
  POLYMARKET_COLLATERAL_CURRENCY,
  POLYMARKET_TRADING_CONFIG,
  REAL_TRADING_ENABLED,
} from './polymarket';

describe('polymarket frontend config', () => {
  it('exposes current public v2 endpoints and pUSD collateral', () => {
    expect(POLYMARKET_API_ENDPOINTS).toEqual({
      gamma: 'https://gamma-api.polymarket.com',
      data: 'https://data-api.polymarket.com',
      clob: 'https://clob.polymarket.com',
    });
    expect(POLYMARKET_COLLATERAL_CURRENCY).toBe('pUSD');
  });

  it('keeps real trading disabled', () => {
    expect(REAL_TRADING_ENABLED).toBe(false);
    expect(POLYMARKET_TRADING_CONFIG).toMatchObject({
      enabled: false,
      mode: 'disabled-read-only-viewer',
      collateralCurrency: 'pUSD',
    });
  });
});

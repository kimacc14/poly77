"""Kalshi API integration for prediction market data."""
import os
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)


def retry_with_backoff(max_retries=3, backoff_factor=2):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Retry {attempt+1}/{max_retries} after {wait_time}s: {e}")
                    time.sleep(wait_time)
        return wrapper
    return decorator


class KalshiClient:
    """Client for fetching data from Kalshi API."""

    BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

    def __init__(self):
        """Initialize Kalshi client."""
        self.api_key = os.getenv("KALSHI_API_KEY")
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'AI-Mindshare-Analyzer/1.0'
        })

        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })
        logger.info("Kalshi client initialized successfully")

    @retry_with_backoff(max_retries=3)
    def get_markets(
        self,
        limit: int = 100,
        status: str = "open",
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch list of markets from Kalshi using events endpoint.

        Args:
            limit: Maximum number of markets to return
            status: Market status ('open', 'closed', 'settled')
            category: Filter by category (e.g., 'politics', 'crypto')

        Returns:
            List of market dictionaries
        """
        try:
            params = {
                "limit": limit,
                "status": status,
                "with_nested_markets": "true"
            }
            if category:
                params["series_ticker"] = category

            response = self.session.get(
                f"{self.BASE_URL}/events",
                params=params,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()
            events = data.get("events", [])

            # Extract markets from events and normalize
            processed_markets = []
            from datetime import timezone
            now = datetime.now(timezone.utc)

            for event in events:
                series_ticker = event.get('series_ticker', '')
                markets = event.get('markets', [])

                for market in markets:
                    # Filter by close time if status is open
                    close_time_str = market.get('close_time')
                    if status == "open" and close_time_str:
                        try:
                            close_time = self._parse_datetime(close_time_str)
                            if close_time and close_time <= now:
                                continue  # Skip expired
                        except Exception:
                            pass

                    # Calculate yes price with fallback
                    yes_price = 0.0
                    try:
                        last_price = market.get("last_price_dollars")
                        if last_price and float(last_price) > 0:
                            yes_price = float(last_price)
                        else:
                            yes_bid = float(market.get("yes_bid_dollars", 0.0) or 0.0)
                            yes_ask = float(market.get("yes_ask_dollars", 0.0) or 0.0)

                            if yes_bid > 0 and yes_ask > 0:
                                yes_price = (yes_bid + yes_ask) / 2
                            elif yes_ask > 0:
                                yes_price = yes_ask
                            elif yes_bid > 0:
                                yes_price = yes_bid
                    except (ValueError, TypeError):
                        yes_price = 0.0

                    # Get volume in cents and convert to dollars
                    volume_cents = market.get("volume", 0) or 0
                    volume_dollars = volume_cents / 100.0

                    # Filter: Only include markets with volume >= $10,000
                    # Note: Kalshi volumes are MUCH lower than Polymarket
                    # Highest observed: ~$660, so use $10 threshold
                    if volume_dollars < 10:  # $10 minimum volume
                        continue

                    # Format close time
                    try:
                        close_time = self._parse_datetime(close_time_str)
                        close_time_formatted = close_time.strftime('%b %d, %Y') if close_time else 'TBD'
                    except Exception:
                        close_time_formatted = 'TBD'

                    ticker = market.get('ticker', '')

                    # Normalize category to lowercase for consistency
                    raw_category = market.get('category', '').lower()
                    # Map Kalshi categories to standard categories
                    category_map = {
                        'politics': 'politics',
                        'crypto': 'cryptocurrency',
                        'cryptocurrency': 'cryptocurrency',
                        'tech': 'technology',
                        'technology': 'technology',
                        'sports': 'sports',
                        'finance': 'finance',
                        'economics': 'finance',
                        'culture': 'other',
                        'science': 'technology',
                        'climate': 'other'
                    }
                    normalized_category = category_map.get(raw_category, raw_category or 'other')

                    processed_markets.append({
                        'platform': 'kalshi',
                        'market_id': ticker,
                        'title': market.get('title', ''),
                        'description': market.get('subtitle', ''),
                        'category': normalized_category,
                        'current_probability': yes_price,
                        'volume': volume_dollars,
                        'end_date': close_time_str,
                        'end_date_formatted': close_time_formatted,
                        'status': market.get('status', 'unknown'),
                        'close_time': self._parse_datetime(close_time_str),
                        'metadata': {
                            'ticker': ticker,
                            'series_ticker': series_ticker,
                            'slug': series_ticker.lower() if series_ticker else ticker.lower(),
                            'open_interest': market.get('open_interest', 0),
                            'yes_bid_dollars': market.get('yes_bid_dollars', 0),
                            'yes_ask_dollars': market.get('yes_ask_dollars', 0),
                            'no_bid_dollars': market.get('no_bid_dollars', 0),
                            'no_ask_dollars': market.get('no_ask_dollars', 0)
                        }
                    })

            logger.info(f"Fetched {len(processed_markets)} markets from {len(events)} Kalshi events")
            return processed_markets

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Kalshi markets: {e}")
            raise

    @retry_with_backoff(max_retries=3)
    def get_market_details(self, market_ticker: str) -> Optional[Dict]:
        """
        Get detailed information for a specific market.

        Args:
            market_ticker: Market ticker/ID

        Returns:
            Market details dictionary
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/markets/{market_ticker}",
                timeout=10
            )
            response.raise_for_status()

            market = response.json().get("market", {})

            return {
                'platform': 'kalshi',
                'market_id': market.get('ticker'),
                'title': market.get('title'),
                'description': market.get('subtitle', ''),
                'category': market.get('category', ''),
                'current_probability': market.get('yes_ask', 0) / 100.0,
                'volume': market.get('volume', 0),
                'close_time': self._parse_datetime(market.get('close_time')),
                'metadata': {
                    'open_interest': market.get('open_interest', 0),
                    'liquidity': market.get('liquidity', 0),
                    'yes_bid': market.get('yes_bid', 0),
                    'yes_ask': market.get('yes_ask', 0),
                    'no_bid': market.get('no_bid', 0),
                    'no_ask': market.get('no_ask', 0),
                    'rules': market.get('rules', ''),
                    'can_close_early': market.get('can_close_early', False)
                }
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Kalshi market {market_ticker}: {e}")
            return None

    def get_market_history(
        self,
        market_ticker: str,
        min_ts: Optional[int] = None,
        max_ts: Optional[int] = None
    ) -> List[Dict]:
        """
        Get historical price data for a market.

        Args:
            market_ticker: Market ticker
            min_ts: Minimum timestamp (Unix)
            max_ts: Maximum timestamp (Unix)

        Returns:
            List of historical data points
        """
        try:
            params = {}
            if min_ts:
                params['min_ts'] = min_ts
            if max_ts:
                params['max_ts'] = max_ts

            response = self.session.get(
                f"{self.BASE_URL}/markets/{market_ticker}/history",
                params=params,
                timeout=10
            )
            response.raise_for_status()

            history = response.json().get("history", [])
            return history

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching market history: {e}")
            return []

    def get_markets_by_category(self, categories: List[str]) -> Dict[str, List[Dict]]:
        """
        Fetch markets grouped by categories.

        Args:
            categories: List of category names

        Returns:
            Dictionary mapping category to list of markets
        """
        results = {}
        for category in categories:
            try:
                markets = self.get_markets(limit=50, category=category)
                results[category] = markets
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                logger.error(f"Error fetching category '{category}': {e}")
                results[category] = []

        return results

    def get_market_url(self, market_data: Dict) -> str:
        """
        Get the URL to trade on Kalshi.

        Args:
            market_data: Market dictionary with metadata

        Returns:
            URL string
        """
        # Prefer series_ticker for direct event URLs
        series_ticker = market_data.get('metadata', {}).get('series_ticker', '')
        if series_ticker:
            return f"https://kalshi.com/markets/{series_ticker.lower()}"

        # Fallback to ticker
        ticker = market_data.get('market_id', '')
        if ticker:
            return f"https://kalshi.com/markets/{ticker.lower()}"

        return "https://kalshi.com"

    @staticmethod
    def _parse_datetime(dt_string: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not dt_string:
            return None
        try:
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except Exception:
            return None


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test client
    client = KalshiClient()

    # Fetch markets
    markets = client.get_markets(limit=10)
    print(f"\nFetched {len(markets)} markets")

    if markets:
        print(f"\nSample market: {markets[0]['title']}")
        print(f"Probability: {markets[0]['current_probability']:.2%}")
        print(f"URL: {client.get_market_url(markets[0]['market_id'])}")

"""Polymarket GraphQL API integration for prediction market data."""
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


class PolymarketClient:
    """Client for fetching data from Polymarket GraphQL API."""

    def __init__(self):
        """Initialize Polymarket client."""
        # Use public Gamma API (no auth required)
        self.gamma_url = "https://gamma-api.polymarket.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        logger.info("Polymarket client initialized successfully (using Gamma API)")

    @retry_with_backoff(max_retries=3)
    def get_markets(
        self,
        limit: int = 100,
        active: bool = True,
        offset: int = 0
    ) -> List[Dict]:
        """
        Fetch markets from Polymarket using Gamma API.

        Args:
            limit: Maximum number of markets
            active: Only active markets
            offset: Pagination offset

        Returns:
            List of market dictionaries
        """
        try:
            # Use Gamma API events endpoint
            url = f"{self.gamma_url}/events"
            params = {'limit': limit}
            if active:
                params['closed'] = 'false'  # Get only open markets

            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()

            events_data = response.json()

            # Events data is a list
            if not isinstance(events_data, list):
                logger.warning(f"Unexpected response format: {type(events_data)}")
                return []

            # Filter for truly active markets (end date in future)
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)

            active_events = []
            for event in events_data:
                end_date_str = event.get('endDate')
                if end_date_str:
                    try:
                        end_date = self._parse_datetime(end_date_str)
                        if end_date and end_date > now:
                            active_events.append(event)
                    except Exception:
                        continue

            logger.info(f"Filtered to {len(active_events)} active events (from {len(events_data)} total)")

            # Process events
            processed_markets = []
            for event in active_events[:limit]:
                # Get the first market in the event
                markets = event.get('markets', [])
                if not markets:
                    continue

                # Use first market for probability
                first_market = markets[0]

                # Parse outcome prices
                try:
                    outcome_prices_str = first_market.get('outcomePrices', '[]')
                    if isinstance(outcome_prices_str, str):
                        import json
                        outcome_prices = json.loads(outcome_prices_str)
                    else:
                        outcome_prices = outcome_prices_str

                    probability = float(outcome_prices[0]) if outcome_prices else 0.5
                except (ValueError, IndexError, TypeError):
                    probability = 0.5

                # Categorize based on description
                title = event.get('title', '')
                description = event.get('description', '')
                category = self._categorize_market(title, description)

                # Filter: Only include markets with volume >= $1,000
                volume = float(event.get('volume', 0))
                if volume < 1000:
                    continue

                processed_markets.append({
                    'platform': 'polymarket',
                    'market_id': str(event.get('id', '')),
                    'title': title,
                    'description': description,
                    'category': category,
                    'current_probability': probability,
                    'volume': volume,
                    'close_time': self._parse_datetime(event.get('endDate')),
                    'metadata': {
                        'outcomes': json.loads(first_market.get('outcomes', '[]')) if isinstance(first_market.get('outcomes'), str) else first_market.get('outcomes', []),
                        'outcome_prices': outcome_prices,
                        'liquidity': float(event.get('liquidity', 0)),
                        'slug': event.get('slug', ''),  # Event slug for URL
                        'resolved_at': None
                    }
                })

            logger.info(f"Fetched {len(processed_markets)} events from Polymarket Gamma API")
            return processed_markets

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Polymarket events: {e}")
            return []  # Return empty list instead of raising

    @retry_with_backoff(max_retries=3)
    def get_market_details(self, market_id: str) -> Optional[Dict]:
        """
        Get detailed information for a specific market.

        Args:
            market_id: Market ID

        Returns:
            Market details dictionary
        """
        query = """
        query Market($id: ID!) {
            market(id: $id) {
                id
                question
                description
                outcomes
                outcomePrices
                volume
                liquidity
                endDate
                resolvedAt
                category
                slug
                tags
                image
            }
        }
        """

        variables = {"id": market_id}

        try:
            response = self.session.post(
                self.api_url,
                json={"query": query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            market = data.get("data", {}).get("market", {})

            if not market:
                return None

            outcome_prices = market.get('outcomePrices', [])
            probability = float(outcome_prices[0]) if outcome_prices else 0.5

            return {
                'platform': 'polymarket',
                'market_id': market.get('id'),
                'title': market.get('question'),
                'description': market.get('description', ''),
                'category': market.get('category', ''),
                'current_probability': probability,
                'volume': float(market.get('volume', 0)),
                'close_time': self._parse_datetime(market.get('endDate')),
                'metadata': {
                    'outcomes': market.get('outcomes', []),
                    'outcome_prices': outcome_prices,
                    'liquidity': market.get('liquidity', 0),
                    'slug': market.get('slug', ''),
                    'resolved_at': market.get('resolvedAt'),
                    'tags': market.get('tags', []),
                    'image': market.get('image', '')
                }
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Polymarket market {market_id}: {e}")
            return None

    @retry_with_backoff(max_retries=3)
    def search_markets(self, search_term: str, limit: int = 50) -> List[Dict]:
        """
        Search markets by keyword.

        Args:
            search_term: Search query
            limit: Maximum results

        Returns:
            List of matching markets
        """
        # Note: Actual GraphQL schema may vary - this is a simplified implementation
        # You may need to fetch all markets and filter locally
        all_markets = self.get_markets(limit=limit * 2)

        # Filter by search term in title or description
        search_lower = search_term.lower()
        matching_markets = [
            m for m in all_markets
            if search_lower in m['title'].lower() or
               search_lower in m.get('description', '').lower()
        ]

        return matching_markets[:limit]

    def get_markets_by_category(self, categories: List[str]) -> Dict[str, List[Dict]]:
        """
        Fetch markets grouped by categories.

        Args:
            categories: List of category names

        Returns:
            Dictionary mapping category to list of markets
        """
        # Fetch all markets and filter by category
        all_markets = self.get_markets(limit=200)

        results = {}
        for category in categories:
            category_lower = category.lower()
            results[category] = [
                m for m in all_markets
                if m.get('category', '').lower() == category_lower
            ]
            logger.info(f"Found {len(results[category])} markets in category '{category}'")

        return results

    def get_market_url(self, market_slug: str) -> str:
        """
        Get the URL to trade on Polymarket.

        Args:
            market_slug: Market slug from metadata

        Returns:
            URL string
        """
        if market_slug:
            return f"https://polymarket.com/event/{market_slug}"
        return "https://polymarket.com/"

    @staticmethod
    def _categorize_market(question: str, description: str) -> str:
        """Categorize market based on keywords in question/description."""
        text = f"{question} {description}".lower()

        if any(word in text for word in ['election', 'president', 'vote', 'senate', 'congress', 'political']):
            return 'politics'
        elif any(word in text for word in ['bitcoin', 'crypto', 'ethereum', 'btc', 'eth', 'blockchain']):
            return 'cryptocurrency'
        elif any(word in text for word in ['nba', 'nfl', 'soccer', 'football', 'baseball', 'sports', 'championship']):
            return 'sports'
        elif any(word in text for word in ['tech', 'ai', 'technology', 'software', 'apple', 'google', 'microsoft']):
            return 'technology'
        else:
            return 'other'

    @staticmethod
    def _parse_datetime(dt_string: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not dt_string:
            return None
        try:
            # Handle Unix timestamp (milliseconds)
            if isinstance(dt_string, int) or (isinstance(dt_string, str) and dt_string.isdigit()):
                return datetime.fromtimestamp(int(dt_string) / 1000)
            # Handle ISO format
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except Exception as e:
            logger.warning(f"Error parsing datetime '{dt_string}': {e}")
            return None


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test client
    client = PolymarketClient()

    # Fetch markets
    markets = client.get_markets(limit=10)
    print(f"\nFetched {len(markets)} markets")

    if markets:
        print(f"\nSample market: {markets[0]['title']}")
        print(f"Probability: {markets[0]['current_probability']:.2%}")
        slug = markets[0]['metadata'].get('slug', '')
        print(f"URL: {client.get_market_url(slug)}")

    # Search markets
    search_results = client.search_markets("election", limit=5)
    print(f"\nFound {len(search_results)} markets matching 'election'")

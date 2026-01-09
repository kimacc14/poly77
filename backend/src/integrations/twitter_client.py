"""Twitter (X) API integration for fetching social data."""
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

# Import mock data generator
try:
    from integrations.mock_data_generator import MockDataGenerator
except ImportError:
    from .mock_data_generator import MockDataGenerator


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


class TwitterClient:
    """Client for fetching data from Twitter API with mock data fallback."""

    def __init__(self, use_mock: bool = None):
        """
        Initialize Twitter client.

        Args:
            use_mock: If True, use mock data. If None, auto-detect based on env var.
        """
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        # Auto-detect mock mode
        if use_mock is None:
            use_mock = not bearer_token or bearer_token == "mock"

        self.use_mock = use_mock
        self.mock_generator = MockDataGenerator() if use_mock else None

        if not self.use_mock:
            try:
                import tweepy
                self.client = tweepy.Client(bearer_token=bearer_token)
                logger.info("Twitter client initialized with real API")
            except Exception as e:
                logger.warning(f"Failed to initialize Twitter API, using mock mode: {e}")
                self.use_mock = True
                self.mock_generator = MockDataGenerator()
        else:
            logger.info("Twitter client initialized in MOCK MODE")

    def search_recent_tweets(
        self,
        query: str,
        max_results: int = 100,
        hours_back: int = 24
    ) -> List[Dict]:
        """
        Search for recent tweets matching query.

        Args:
            query: Search query (keywords, hashtags, etc.)
            max_results: Maximum number of tweets to return (10-100)
            hours_back: How many hours back to search

        Returns:
            List of tweet dictionaries with text, metrics, timestamp
        """
        # Use mock data if in mock mode
        if self.use_mock:
            logger.info(f"Using MOCK data for query: {query}")
            return self.mock_generator.generate_mock_tweets(
                topic=query,
                count=max_results,
                hours_back=hours_back
            )

        # Real API call
        try:
            import tweepy

            # Calculate start time
            start_time = datetime.utcnow() - timedelta(hours=hours_back)

            # Search tweets
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                start_time=start_time,
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'lang'],
                expansions=['author_id'],
                user_fields=['username', 'public_metrics', 'verified']
            )

            if not response.data:
                logger.info(f"No tweets found for query: {query}")
                return []

            # Extract user data
            users = {user.id: user for user in response.includes.get('users', [])} if response.includes else {}

            # Process tweets
            tweets = []
            for tweet in response.data:
                user = users.get(tweet.author_id)
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'likes': tweet.public_metrics['like_count'],
                    'retweets': tweet.public_metrics['retweet_count'],
                    'replies': tweet.public_metrics['reply_count'],
                    'author_id': tweet.author_id,
                    'author_username': user.username if user else None,
                    'author_followers': user.public_metrics['followers_count'] if user else 0,
                    'author_verified': user.verified if user else False,
                    'language': tweet.lang,
                    'platform': 'twitter'
                })

            logger.info(f"Fetched {len(tweets)} tweets for query: {query}")
            return tweets

        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            # Fallback to mock data
            logger.warning("Falling back to mock data")
            self.use_mock = True
            self.mock_generator = MockDataGenerator()
            return self.mock_generator.generate_mock_tweets(query, max_results, hours_back)

    def fetch_topics_data(self, topics: List[str], hours_back: int = 24) -> Dict[str, List[Dict]]:
        """
        Fetch tweets for multiple topics.

        Args:
            topics: List of search topics/keywords
            hours_back: How many hours back to search

        Returns:
            Dictionary mapping topic to list of tweets
        """
        results = {}
        for topic in topics:
            try:
                tweets = self.search_recent_tweets(topic, max_results=100, hours_back=hours_back)
                results[topic] = tweets
                # Rate limiting delay
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error fetching tweets for topic '{topic}': {e}")
                results[topic] = []

        return results

    def get_trending_topics(self, location_id: int = 1) -> List[str]:
        """
        Get trending topics (requires elevated access).

        Args:
            location_id: WOEID location ID (1 = worldwide)

        Returns:
            List of trending topic names
        """
        # Note: This requires v1.1 API and elevated access
        # For v2 API, this functionality is limited
        logger.warning("Trending topics require Twitter API v1.1 elevated access")
        return []


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test client
    client = TwitterClient()

    # Search for election-related tweets
    topics = ["2026 election", "Bitcoin regulation", "AI policy"]
    results = client.fetch_topics_data(topics, hours_back=12)

    for topic, tweets in results.items():
        print(f"\n{topic}: {len(tweets)} tweets")
        if tweets:
            print(f"Sample: {tweets[0]['text'][:100]}...")

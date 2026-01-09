"""Reddit API integration for fetching social data."""
import os
import requests
from typing import List, Dict, Optional
from datetime import datetime
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


class RedditClient:
    """Client for fetching data from Reddit API with public JSON and mock fallback."""

    def __init__(self, use_mock: bool = None, use_public_json: bool = True):
        """
        Initialize Reddit client.

        Args:
            use_mock: If True, use mock data. If None, auto-detect.
            use_public_json: If True, use public JSON endpoint (no auth needed).
        """
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT", "MindshareAnalyzer/1.0")

        # Auto-detect mock mode
        if use_mock is None:
            use_mock = not client_id or client_id == "mock"

        self.use_mock = use_mock
        self.use_public_json = use_public_json
        self.mock_generator = MockDataGenerator() if use_mock else None
        self.user_agent = user_agent

        if not self.use_mock and not self.use_public_json:
            try:
                import praw
                self.reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                logger.info("Reddit client initialized with PRAW")
            except Exception as e:
                logger.warning(f"Failed to initialize PRAW, using public JSON: {e}")
                self.use_public_json = True
        elif self.use_public_json:
            logger.info("Reddit client initialized with PUBLIC JSON (no auth)")
        else:
            logger.info("Reddit client initialized in MOCK MODE")

    @retry_with_backoff(max_retries=3)
    def search_posts(
        self,
        query: str,
        subreddit: Optional[str] = None,
        time_filter: str = "day",
        limit: int = 100
    ) -> List[Dict]:
        """
        Search for posts matching query.

        Args:
            query: Search query
            subreddit: Specific subreddit to search (None for all)
            time_filter: 'hour', 'day', 'week', 'month', 'year', 'all'
            limit: Maximum number of posts to return

        Returns:
            List of post dictionaries with text, metrics, timestamp
        """
        try:
            if subreddit:
                search_target = self.reddit.subreddit(subreddit)
            else:
                search_target = self.reddit.subreddit("all")

            posts = []
            for submission in search_target.search(query, time_filter=time_filter, limit=limit):
                # Get top comments for additional context
                submission.comments.replace_more(limit=0)
                top_comments = [
                    comment.body for comment in submission.comments.list()[:5]
                ]

                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'subreddit': submission.subreddit.display_name,
                    'created_at': datetime.fromtimestamp(submission.created_utc),
                    'upvotes': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'num_comments': submission.num_comments,
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'url': submission.url,
                    'top_comments': top_comments,
                    'platform': 'reddit'
                })

            logger.info(f"Fetched {len(posts)} posts for query: {query}")
            return posts

        except Exception as e:
            logger.error(f"Error fetching Reddit posts: {e}")
            raise

    @retry_with_backoff(max_retries=3)
    def get_subreddit_posts(
        self,
        subreddit: str,
        sort: str = "hot",
        time_filter: str = "day",
        limit: int = 100
    ) -> List[Dict]:
        """
        Get posts from specific subreddit.

        Args:
            subreddit: Subreddit name
            sort: 'hot', 'new', 'top', 'rising', 'controversial'
            time_filter: For 'top' and 'controversial' sorts
            limit: Maximum number of posts

        Returns:
            List of post dictionaries
        """
        try:
            sub = self.reddit.subreddit(subreddit)

            # Get posts based on sort method
            if sort == "hot":
                submissions = sub.hot(limit=limit)
            elif sort == "new":
                submissions = sub.new(limit=limit)
            elif sort == "top":
                submissions = sub.top(time_filter=time_filter, limit=limit)
            elif sort == "rising":
                submissions = sub.rising(limit=limit)
            elif sort == "controversial":
                submissions = sub.controversial(time_filter=time_filter, limit=limit)
            else:
                raise ValueError(f"Invalid sort method: {sort}")

            posts = []
            for submission in submissions:
                submission.comments.replace_more(limit=0)
                top_comments = [
                    comment.body for comment in submission.comments.list()[:5]
                ]

                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'subreddit': submission.subreddit.display_name,
                    'created_at': datetime.fromtimestamp(submission.created_utc),
                    'upvotes': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'num_comments': submission.num_comments,
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'url': submission.url,
                    'top_comments': top_comments,
                    'platform': 'reddit'
                })

            logger.info(f"Fetched {len(posts)} posts from r/{subreddit}")
            return posts

        except Exception as e:
            logger.error(f"Error fetching subreddit posts: {e}")
            raise

    def fetch_topics_data(
        self,
        topics: List[str],
        relevant_subreddits: Optional[List[str]] = None,
        time_filter: str = "day"
    ) -> Dict[str, List[Dict]]:
        """
        Fetch posts for multiple topics from relevant subreddits.

        Args:
            topics: List of search topics
            relevant_subreddits: List of subreddits to search (None for all)
            time_filter: Time range for posts

        Returns:
            Dictionary mapping topic to list of posts
        """
        results = {}

        # Default subreddits for different categories
        if not relevant_subreddits:
            relevant_subreddits = [
                'politics', 'worldnews', 'news',
                'cryptocurrency', 'CryptoMarkets',
                'technology', 'sports'
            ]

        for topic in topics:
            all_posts = []
            for subreddit in relevant_subreddits:
                try:
                    posts = self.search_posts(
                        query=topic,
                        subreddit=subreddit,
                        time_filter=time_filter,
                        limit=50
                    )
                    all_posts.extend(posts)
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error fetching r/{subreddit} for topic '{topic}': {e}")

            results[topic] = all_posts
            logger.info(f"Total {len(all_posts)} posts for topic: {topic}")

        return results


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test client
    client = RedditClient()

    # Search for topics
    topics = ["2026 election", "Bitcoin regulation"]
    results = client.fetch_topics_data(topics, time_filter="day")

    for topic, posts in results.items():
        print(f"\n{topic}: {len(posts)} posts")
        if posts:
            print(f"Sample: {posts[0]['title']}")

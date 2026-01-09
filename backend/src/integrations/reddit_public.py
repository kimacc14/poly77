"""Reddit public JSON API - no authentication required."""
import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


class RedditPublicClient:
    """Client for Reddit public JSON API (no auth needed)."""

    def __init__(self):
        """Initialize Reddit public client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MindshareAnalyzer/1.0 (Educational/Research)'
        })
        logger.info("Reddit public JSON client initialized")

    def search_posts(
        self,
        query: str,
        subreddit: str = "all",
        time_filter: str = "day",
        limit: int = 100
    ) -> List[Dict]:
        """
        Search Reddit posts using public JSON endpoint.

        Args:
            query: Search query
            subreddit: Subreddit name (default: "all")
            time_filter: 'hour', 'day', 'week', 'month', 'year'
            limit: Maximum posts to return

        Returns:
            List of post dictionaries
        """
        try:
            url = f"https://www.reddit.com/r/{subreddit}/search.json"
            params = {
                'q': query,
                't': time_filter,
                'limit': min(limit, 100),
                'sort': 'relevance',
                'restrict_sr': 'on' if subreddit != 'all' else 'off'
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            posts = []

            for child in data.get('data', {}).get('children', []):
                post_data = child.get('data', {})

                posts.append({
                    'id': post_data.get('id'),
                    'title': post_data.get('title', ''),
                    'text': post_data.get('selftext', ''),
                    'subreddit': post_data.get('subreddit', ''),
                    'created_at': datetime.fromtimestamp(post_data.get('created_utc', 0)),
                    'upvotes': post_data.get('score', 0),
                    'upvote_ratio': post_data.get('upvote_ratio', 0.5),
                    'num_comments': post_data.get('num_comments', 0),
                    'author': post_data.get('author', '[deleted]'),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'top_comments': [],  # Public JSON doesn't include comments
                    'platform': 'reddit'
                })

            logger.info(f"Fetched {len(posts)} posts from r/{subreddit} for query: {query}")
            return posts

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from Reddit: {e}")
            return []

    def get_subreddit_posts(
        self,
        subreddit: str,
        sort: str = "hot",
        time_filter: str = "day",
        limit: int = 100
    ) -> List[Dict]:
        """
        Get posts from a subreddit.

        Args:
            subreddit: Subreddit name
            sort: 'hot', 'new', 'top', 'rising'
            time_filter: For 'top' sort
            limit: Maximum posts

        Returns:
            List of posts
        """
        try:
            if sort == 'top':
                url = f"https://www.reddit.com/r/{subreddit}/top.json"
                params = {'t': time_filter, 'limit': min(limit, 100)}
            else:
                url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
                params = {'limit': min(limit, 100)}

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            posts = []

            for child in data.get('data', {}).get('children', []):
                post_data = child.get('data', {})

                posts.append({
                    'id': post_data.get('id'),
                    'title': post_data.get('title', ''),
                    'text': post_data.get('selftext', ''),
                    'subreddit': post_data.get('subreddit', ''),
                    'created_at': datetime.fromtimestamp(post_data.get('created_utc', 0)),
                    'upvotes': post_data.get('score', 0),
                    'upvote_ratio': post_data.get('upvote_ratio', 0.5),
                    'num_comments': post_data.get('num_comments', 0),
                    'author': post_data.get('author', '[deleted]'),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'top_comments': [],
                    'platform': 'reddit'
                })

            logger.info(f"Fetched {len(posts)} posts from r/{subreddit}")
            return posts

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching subreddit: {e}")
            return []

    def fetch_topics_data(
        self,
        topics: List[str],
        relevant_subreddits: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Fetch posts for multiple topics.

        Args:
            topics: List of topics
            relevant_subreddits: Subreddits to search

        Returns:
            Dict mapping topic to posts
        """
        if not relevant_subreddits:
            relevant_subreddits = [
                'all', 'news', 'worldnews', 'politics',
                'cryptocurrency', 'CryptoMarkets', 'Bitcoin',
                'technology', 'sports'
            ]

        results = {}

        for topic in topics:
            all_posts = []

            for subreddit in relevant_subreddits[:3]:  # Limit to avoid rate limits
                posts = self.search_posts(topic, subreddit, limit=25)
                all_posts.extend(posts)
                time.sleep(2)  # Rate limiting - be respectful

            results[topic] = all_posts
            logger.info(f"Total {len(all_posts)} posts for topic: {topic}")

        return results


# Test if __main__
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    client = RedditPublicClient()

    # Test search
    posts = client.search_posts("Bitcoin", subreddit="cryptocurrency", limit=10)
    print(f"\nFound {len(posts)} posts")

    if posts:
        print(f"Sample: {posts[0]['title']}")
        print(f"Upvotes: {posts[0]['upvotes']}")

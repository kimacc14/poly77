"""Mock data generator for realistic synthetic social media posts."""
from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)
fake = Faker()


class MockDataGenerator:
    """Generate realistic synthetic social media data for testing."""

    # Sentiment templates
    POSITIVE_TEMPLATES = [
        "{topic} is looking great! {sentence}",
        "Bullish on {topic}! {sentence}",
        "{topic} to the moon! {sentence}",
        "Amazing news for {topic}. {sentence}",
        "Very optimistic about {topic}. {sentence}",
    ]

    NEGATIVE_TEMPLATES = [
        "{topic} is disappointing. {sentence}",
        "Bearish on {topic}. {sentence}",
        "Not looking good for {topic}. {sentence}",
        "Concerned about {topic}. {sentence}",
        "Major issues with {topic}. {sentence}",
    ]

    NEUTRAL_TEMPLATES = [
        "Discussing {topic}: {sentence}",
        "Thoughts on {topic}? {sentence}",
        "Analysis of {topic}. {sentence}",
        "Update on {topic}. {sentence}",
        "What do you think about {topic}? {sentence}",
    ]

    def generate_mock_tweets(
        self,
        topic: str,
        count: int,
        hours_back: int = 24,
        sentiment_distribution: Dict[str, float] = None
    ) -> List[Dict]:
        """
        Generate synthetic tweets with realistic structure.

        Args:
            topic: Topic to generate tweets about
            count: Number of tweets to generate
            hours_back: Time range for timestamps
            sentiment_distribution: {'positive': 0.4, 'negative': 0.3, 'neutral': 0.3}

        Returns:
            List of tweet dictionaries matching Twitter API structure
        """
        if sentiment_distribution is None:
            sentiment_distribution = {'positive': 0.4, 'negative': 0.3, 'neutral': 0.3}

        tweets = []
        start_time = datetime.utcnow() - timedelta(hours=hours_back)

        # Generate sentiment pool
        sentiments = []
        for sentiment, ratio in sentiment_distribution.items():
            sentiments.extend([sentiment] * int(count * ratio))
        sentiments.extend(['neutral'] * (count - len(sentiments)))  # Fill remainder
        random.shuffle(sentiments)

        for i in range(count):
            sentiment = sentiments[i]

            # Generate text based on sentiment
            if sentiment == 'positive':
                template = random.choice(self.POSITIVE_TEMPLATES)
            elif sentiment == 'negative':
                template = random.choice(self.NEGATIVE_TEMPLATES)
            else:
                template = random.choice(self.NEUTRAL_TEMPLATES)

            text = template.format(
                topic=topic,
                sentence=fake.sentence(nb_words=random.randint(5, 12))
            )

            # Generate realistic metrics
            followers = random.randint(100, 50000)
            follower_multiplier = min(followers / 1000, 10)

            tweet = {
                'id': fake.uuid4(),
                'text': text,
                'created_at': fake.date_time_between(
                    start_date=start_time,
                    end_date='now'
                ),
                'likes': int(random.randint(0, 100) * follower_multiplier),
                'retweets': int(random.randint(0, 50) * follower_multiplier),
                'replies': int(random.randint(0, 30) * follower_multiplier),
                'author_id': fake.uuid4(),
                'author_username': fake.user_name(),
                'author_followers': followers,
                'author_verified': random.random() < 0.1,  # 10% verified
                'language': 'en',
                'platform': 'twitter'
            }
            tweets.append(tweet)

        logger.info(f"Generated {len(tweets)} mock tweets for topic: {topic}")
        return tweets

    def generate_mock_reddit_posts(
        self,
        topic: str,
        count: int,
        sentiment_distribution: Dict[str, float] = None
    ) -> List[Dict]:
        """
        Generate synthetic Reddit posts.

        Args:
            topic: Topic to generate posts about
            count: Number of posts to generate
            sentiment_distribution: Sentiment ratios

        Returns:
            List of post dictionaries matching Reddit API structure
        """
        if sentiment_distribution is None:
            sentiment_distribution = {'positive': 0.4, 'negative': 0.3, 'neutral': 0.3}

        posts = []
        subreddits = ['all', 'news', 'cryptocurrency', 'politics', 'technology', 'worldnews']

        # Generate sentiment pool
        sentiments = []
        for sentiment, ratio in sentiment_distribution.items():
            sentiments.extend([sentiment] * int(count * ratio))
        sentiments.extend(['neutral'] * (count - len(sentiments)))
        random.shuffle(sentiments)

        for i in range(count):
            sentiment = sentiments[i]

            # Generate title and text based on sentiment
            if sentiment == 'positive':
                title_template = random.choice([
                    f"Why {topic} is the best! {fake.sentence(nb_words=5)}",
                    f"{topic} exceeds expectations. {fake.sentence(nb_words=5)}",
                    f"Great news for {topic}! {fake.sentence(nb_words=5)}"
                ])
            elif sentiment == 'negative':
                title_template = random.choice([
                    f"Problems with {topic}: {fake.sentence(nb_words=5)}",
                    f"Disappointed by {topic}. {fake.sentence(nb_words=5)}",
                    f"Major concerns about {topic}. {fake.sentence(nb_words=5)}"
                ])
            else:
                title_template = random.choice([
                    f"Thoughts on {topic}? {fake.sentence(nb_words=5)}",
                    f"Discussion: {topic}. {fake.sentence(nb_words=5)}",
                    f"Analysis of {topic}. {fake.sentence(nb_words=5)}"
                ])

            text = fake.paragraph(nb_sentences=random.randint(2, 5))

            # Add topic-relevant keywords
            if 'crypto' in topic.lower() or 'bitcoin' in topic.lower():
                text += f" Blockchain technology and {topic} are changing the landscape."
            elif 'election' in topic.lower() or 'politic' in topic.lower():
                text += f" The political implications of {topic} are significant."

            post = {
                'id': fake.uuid4(),
                'title': title_template,
                'text': text,
                'subreddit': random.choice(subreddits),
                'created_at': fake.date_time_between(start_date='-24h', end_date='now'),
                'upvotes': random.randint(0, 1000),
                'upvote_ratio': random.uniform(0.5, 0.95),
                'num_comments': random.randint(0, 200),
                'author': fake.user_name(),
                'url': f"https://reddit.com/r/{random.choice(subreddits)}/comments/{fake.uuid4()}",
                'top_comments': [fake.sentence(nb_words=10) for _ in range(random.randint(0, 3))],
                'platform': 'reddit'
            }
            posts.append(post)

        logger.info(f"Generated {len(posts)} mock Reddit posts for topic: {topic}")
        return posts

    def generate_combined_mock_data(
        self,
        topic: str,
        tweet_count: int = 50,
        reddit_count: int = 50
    ) -> Dict[str, List[Dict]]:
        """
        Generate both Twitter and Reddit mock data.

        Returns:
            {'twitter': [...], 'reddit': [...]}
        """
        return {
            'twitter': self.generate_mock_tweets(topic, tweet_count),
            'reddit': self.generate_mock_reddit_posts(topic, reddit_count)
        }


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    generator = MockDataGenerator()

    # Generate mock data
    tweets = generator.generate_mock_tweets("Bitcoin regulation", 20)
    posts = generator.generate_mock_reddit_posts("Bitcoin regulation", 20)

    print(f"\nGenerated {len(tweets)} tweets")
    print(f"Sample tweet: {tweets[0]['text']}")

    print(f"\nGenerated {len(posts)} Reddit posts")
    print(f"Sample post: {posts[0]['title']}")

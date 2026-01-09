"""AI-powered sentiment analysis service using transformers."""
import logging
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Sentiment analysis using Hugging Face transformers."""

    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment"):
        """
        Initialize sentiment analyzer with pre-trained model.

        Args:
            model_name: Hugging Face model identifier
        """
        try:
            logger.info(f"Loading sentiment model: {model_name}")

            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

            # Create pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )

            logger.info("Sentiment analyzer initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing sentiment analyzer: {e}")
            raise

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with sentiment label and score
        """
        try:
            if not text or len(text.strip()) == 0:
                return {'label': 'NEUTRAL', 'score': 0.0, 'normalized_score': 0.0}

            # Truncate if too long
            text = text[:512]

            result = self.sentiment_pipeline(text)[0]

            # Normalize score to -1 to +1 scale
            label = result['label'].upper()
            score = result['score']

            if 'POSITIVE' in label or 'POS' in label:
                normalized_score = score
            elif 'NEGATIVE' in label or 'NEG' in label:
                normalized_score = -score
            else:  # NEUTRAL
                normalized_score = 0.0

            return {
                'label': label,
                'score': score,
                'normalized_score': normalized_score
            }

        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return {'label': 'NEUTRAL', 'score': 0.0, 'normalized_score': 0.0}

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment of multiple texts in batch.

        Args:
            texts: List of texts to analyze

        Returns:
            List of sentiment dictionaries
        """
        try:
            if not texts:
                return []

            # Filter and truncate texts
            valid_texts = [t[:512] for t in texts if t and len(t.strip()) > 0]

            if not valid_texts:
                return []

            # Batch inference
            results = self.sentiment_pipeline(valid_texts)

            # Normalize scores
            normalized_results = []
            for result in results:
                label = result['label'].upper()
                score = result['score']

                if 'POSITIVE' in label or 'POS' in label:
                    normalized_score = score
                elif 'NEGATIVE' in label or 'NEG' in label:
                    normalized_score = -score
                else:
                    normalized_score = 0.0

                normalized_results.append({
                    'label': label,
                    'score': score,
                    'normalized_score': normalized_score
                })

            return normalized_results

        except Exception as e:
            logger.error(f"Error analyzing batch: {e}")
            return [{'label': 'NEUTRAL', 'score': 0.0, 'normalized_score': 0.0}] * len(texts)

    def analyze_social_posts(self, posts: List[Dict]) -> Dict:
        """
        Analyze sentiment of social media posts and calculate aggregate metrics.

        Args:
            posts: List of post dictionaries from Twitter/Reddit

        Returns:
            Aggregated sentiment metrics
        """
        if not posts:
            return {
                'sentiment_score': 0.0,
                'mention_count': 0,
                'engagement_score': 0.0,
                'positive_ratio': 0.0,
                'negative_ratio': 0.0,
                'neutral_ratio': 0.0
            }

        # Extract texts
        texts = []
        for post in posts:
            if post.get('platform') == 'twitter':
                texts.append(post.get('text', ''))
            elif post.get('platform') == 'reddit':
                # Combine title and text
                title = post.get('title', '')
                text = post.get('text', '')
                texts.append(f"{title} {text}")

        # Analyze sentiments
        sentiments = self.analyze_batch(texts)

        # Calculate weighted sentiment score (weight by engagement)
        weighted_scores = []
        total_weight = 0

        for post, sentiment in zip(posts, sentiments):
            # Calculate engagement weight
            if post.get('platform') == 'twitter':
                engagement = (
                    post.get('likes', 0) +
                    post.get('retweets', 0) * 2 +
                    post.get('replies', 0)
                )
                # Boost for verified accounts with many followers
                if post.get('author_verified'):
                    engagement *= 1.5
                follower_boost = min(post.get('author_followers', 0) / 10000, 2.0)
                engagement *= (1 + follower_boost)

            elif post.get('platform') == 'reddit':
                engagement = (
                    post.get('upvotes', 0) * post.get('upvote_ratio', 1.0) +
                    post.get('num_comments', 0) * 2
                )

            else:
                engagement = 1

            weight = max(engagement, 1)  # Minimum weight of 1
            weighted_scores.append(sentiment['normalized_score'] * weight)
            total_weight += weight

        # Calculate average weighted sentiment
        if total_weight > 0:
            avg_sentiment = sum(weighted_scores) / total_weight
        else:
            avg_sentiment = 0.0

        # Calculate ratios
        positive_count = sum(1 for s in sentiments if s['normalized_score'] > 0.3)
        negative_count = sum(1 for s in sentiments if s['normalized_score'] < -0.3)
        neutral_count = len(sentiments) - positive_count - negative_count

        total_count = len(sentiments)
        positive_ratio = positive_count / total_count if total_count > 0 else 0
        negative_ratio = negative_count / total_count if total_count > 0 else 0
        neutral_ratio = neutral_count / total_count if total_count > 0 else 0

        # Calculate engagement score
        if post.get('platform') == 'twitter':
            total_engagement = sum(
                p.get('likes', 0) + p.get('retweets', 0) + p.get('replies', 0)
                for p in posts
            )
        else:
            total_engagement = sum(p.get('upvotes', 0) for p in posts)

        return {
            'sentiment_score': round(avg_sentiment, 3),
            'mention_count': len(posts),
            'engagement_score': total_engagement,
            'positive_ratio': round(positive_ratio, 3),
            'negative_ratio': round(negative_ratio, 3),
            'neutral_ratio': round(neutral_ratio, 3),
            'timestamp': datetime.utcnow()
        }


class MindshareCalculator:
    """Calculate mindshare metrics from social data."""

    @staticmethod
    def calculate_mindshare(
        current_metrics: Dict,
        historical_avg: Optional[Dict] = None
    ) -> float:
        """
        Calculate mindshare score (0-1 scale).

        Args:
            current_metrics: Current sentiment metrics
            historical_avg: Historical average metrics for normalization

        Returns:
            Mindshare score
        """
        # Extract metrics
        mention_count = current_metrics.get('mention_count', 0)
        sentiment_score = current_metrics.get('sentiment_score', 0.0)
        engagement = current_metrics.get('engagement_score', 0)

        # Normalize mention volume (0-1)
        if historical_avg and historical_avg.get('mention_count', 0) > 0:
            normalized_volume = min(
                mention_count / historical_avg['mention_count'],
                2.0
            ) / 2.0
        else:
            normalized_volume = min(mention_count / 100, 1.0)

        # Weighted sentiment (convert -1 to +1 range to 0 to 1)
        weighted_sentiment = (sentiment_score + 1) / 2

        # Normalize engagement (0-1)
        if historical_avg and historical_avg.get('engagement_score', 0) > 0:
            normalized_engagement = min(
                engagement / historical_avg['engagement_score'],
                2.0
            ) / 2.0
        else:
            normalized_engagement = min(engagement / 1000, 1.0)

        # Calculate mindshare score
        mindshare = (
            0.4 * normalized_volume +
            0.3 * weighted_sentiment +
            0.3 * normalized_engagement
        )

        return round(mindshare, 3)

    @staticmethod
    def calculate_sentiment_velocity(
        current_score: float,
        previous_score: float,
        time_delta_hours: float
    ) -> float:
        """
        Calculate rate of sentiment change.

        Args:
            current_score: Current sentiment score
            previous_score: Previous sentiment score
            time_delta_hours: Time difference in hours

        Returns:
            Sentiment velocity (change per hour)
        """
        if time_delta_hours <= 0:
            return 0.0

        velocity = (current_score - previous_score) / time_delta_hours
        return round(velocity, 4)


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test analyzer
    analyzer = SentimentAnalyzer()

    # Test single text
    text = "Bitcoin regulation is terrible for innovation and freedom!"
    result = analyzer.analyze_text(text)
    print(f"\nText: {text}")
    print(f"Sentiment: {result['label']} (score: {result['normalized_score']:.3f})")

    # Test batch
    texts = [
        "This election candidate is amazing!",
        "I hate this new policy",
        "The weather is okay today"
    ]
    results = analyzer.analyze_batch(texts)
    for t, r in zip(texts, results):
        print(f"\n{t}: {r['label']} ({r['normalized_score']:.3f})")

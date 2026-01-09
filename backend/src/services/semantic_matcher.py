"""Semantic matching service to connect social insights with prediction markets."""
import logging
from typing import List, Dict, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer, util
import spacy

logger = logging.getLogger(__name__)


class SemanticMatcher:
    """Match social sentiment topics to prediction markets using semantic similarity."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize semantic matcher.

        Args:
            model_name: Sentence transformer model name
        """
        try:
            logger.info(f"Loading sentence transformer: {model_name}")
            self.model = SentenceTransformer(model_name)

            # Load spaCy for entity extraction
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model not found, downloading...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")

            logger.info("Semantic matcher initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing semantic matcher: {e}")
            raise

    def extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities from text.

        Args:
            text: Input text

        Returns:
            List of entity strings
        """
        try:
            doc = self.nlp(text)
            entities = [ent.text.lower() for ent in doc.ents]
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return []

    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0-1)
        """
        try:
            # Encode texts
            embedding1 = self.model.encode(text1, convert_to_tensor=True)
            embedding2 = self.model.encode(text2, convert_to_tensor=True)

            # Compute cosine similarity
            similarity = util.cos_sim(embedding1, embedding2).item()

            return max(0.0, min(1.0, similarity))

        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0

    def match_topic_to_markets(
        self,
        topic: str,
        topic_description: str,
        markets: List[Dict],
        threshold: float = 0.65,
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Match a social topic to relevant prediction markets.

        Args:
            topic: Topic name/keyword
            topic_description: Aggregated description from social posts
            markets: List of market dictionaries
            threshold: Minimum similarity threshold
            top_k: Maximum number of matches to return

        Returns:
            List of (market, similarity_score) tuples
        """
        if not markets:
            return []

        # Create topic query text
        topic_text = f"{topic} {topic_description}"

        # Extract entities from topic
        topic_entities = set(self.extract_entities(topic_text))

        matches = []

        for market in markets:
            # Create market text
            market_text = f"{market['title']} {market.get('description', '')}"

            # Compute semantic similarity
            semantic_sim = self.compute_similarity(topic_text, market_text)

            # Extract market entities
            market_entities = set(self.extract_entities(market_text))

            # Compute entity overlap score (Jaccard similarity)
            if topic_entities and market_entities:
                entity_overlap = len(topic_entities & market_entities) / len(topic_entities | market_entities)
            else:
                entity_overlap = 0.0

            # Combined score (weighted)
            combined_score = 0.7 * semantic_sim + 0.3 * entity_overlap

            # Category boost (if topic keywords match market category)
            if market.get('category'):
                category_lower = market['category'].lower()
                topic_lower = topic.lower()
                if any(word in category_lower for word in topic_lower.split()):
                    combined_score *= 1.1

            # Apply threshold
            if combined_score >= threshold:
                matches.append((market, combined_score))

        # Sort by score (descending) and return top_k
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_k]

    def match_multiple_topics(
        self,
        topics: Dict[str, Dict],
        markets: List[Dict],
        threshold: float = 0.65
    ) -> Dict[str, List[Tuple[Dict, float]]]:
        """
        Match multiple topics to markets.

        Args:
            topics: Dictionary mapping topic name to topic data (with description)
            markets: List of market dictionaries
            threshold: Minimum similarity threshold

        Returns:
            Dictionary mapping topic to list of (market, score) tuples
        """
        results = {}

        for topic_name, topic_data in topics.items():
            description = topic_data.get('description', '')
            matches = self.match_topic_to_markets(
                topic_name,
                description,
                markets,
                threshold=threshold
            )
            results[topic_name] = matches
            logger.info(f"Matched '{topic_name}' to {len(matches)} markets")

        return results

    def create_topic_description(self, posts: List[Dict]) -> str:
        """
        Create a summary description from social posts.

        Args:
            posts: List of social media posts

        Returns:
            Aggregated description string
        """
        # Extract key texts
        texts = []
        for post in posts[:20]:  # Limit to top 20 most engaged posts
            if post.get('platform') == 'twitter':
                texts.append(post.get('text', ''))
            elif post.get('platform') == 'reddit':
                texts.append(f"{post.get('title', '')} {post.get('text', '')}")

        # Combine and truncate
        combined = " ".join(texts)
        return combined[:2000]  # Limit length

    def batch_encode_markets(self, markets: List[Dict]) -> np.ndarray:
        """
        Pre-encode markets for faster matching.

        Args:
            markets: List of market dictionaries

        Returns:
            NumPy array of market embeddings
        """
        try:
            market_texts = [
                f"{m['title']} {m.get('description', '')}"
                for m in markets
            ]
            embeddings = self.model.encode(market_texts, convert_to_tensor=False)
            return np.array(embeddings)

        except Exception as e:
            logger.error(f"Error encoding markets: {e}")
            return np.array([])

    def fast_match_with_preencoded(
        self,
        topic: str,
        topic_description: str,
        markets: List[Dict],
        market_embeddings: np.ndarray,
        threshold: float = 0.65,
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Fast matching using pre-encoded market embeddings.

        Args:
            topic: Topic name
            topic_description: Topic description
            markets: List of markets
            market_embeddings: Pre-computed market embeddings
            threshold: Minimum similarity
            top_k: Maximum matches

        Returns:
            List of (market, score) tuples
        """
        try:
            # Encode topic
            topic_text = f"{topic} {topic_description}"
            topic_embedding = self.model.encode(topic_text, convert_to_tensor=False)

            # Compute similarities
            similarities = util.cos_sim(topic_embedding, market_embeddings)[0].numpy()

            # Find top matches above threshold
            matches = []
            for idx, sim_score in enumerate(similarities):
                if sim_score >= threshold:
                    matches.append((markets[idx], float(sim_score)))

            # Sort and return top_k
            matches.sort(key=lambda x: x[1], reverse=True)
            return matches[:top_k]

        except Exception as e:
            logger.error(f"Error in fast matching: {e}")
            return []


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test matcher
    matcher = SemanticMatcher()

    # Sample market
    markets = [
        {
            'title': 'Will Bitcoin reach $100,000 by end of 2026?',
            'description': 'This market resolves YES if Bitcoin price exceeds $100,000',
            'category': 'cryptocurrency',
            'platform': 'kalshi'
        },
        {
            'title': 'Will Trump win 2026 Senate race?',
            'description': 'Republican candidate election outcome',
            'category': 'politics',
            'platform': 'polymarket'
        }
    ]

    # Sample topic
    topic = "Bitcoin regulation"
    description = "Discussion about new crypto regulations affecting Bitcoin trading and mining"

    # Match
    matches = matcher.match_topic_to_markets(topic, description, markets, threshold=0.3)

    print(f"\nMatches for '{topic}':")
    for market, score in matches:
        print(f"- {market['title']} (score: {score:.3f})")

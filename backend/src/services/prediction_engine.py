"""Market shift prediction engine based on sentiment analysis."""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)


class PredictionEngine:
    """Predict market probability shifts based on sentiment changes."""

    def __init__(self):
        """Initialize prediction engine."""
        self.config = {
            'sentiment_multiplier': 10.0,  # Base shift per sentiment change
            'volume_cap': 2.0,  # Maximum volume factor
            'min_confidence_threshold': 0.4,
            'high_confidence_threshold': 0.7
        }
        logger.info("Prediction engine initialized")

    def predict_market_shift(
        self,
        sentiment_data: Dict,
        market_data: Dict,
        time_horizon: str = '6h'
    ) -> Dict:
        """
        Predict probability shift for a market based on sentiment.

        Args:
            sentiment_data: Current and historical sentiment metrics
            market_data: Market information including current probability
            time_horizon: Prediction timeframe ('1h', '6h', '24h')

        Returns:
            Prediction dictionary with shift, confidence, reasoning
        """
        try:
            # Extract sentiment metrics
            current_sentiment = sentiment_data.get('current_score', 0.0)
            previous_sentiment = sentiment_data.get('previous_score', 0.0)
            sentiment_delta = current_sentiment - previous_sentiment

            current_volume = sentiment_data.get('mention_count', 0)
            avg_volume = sentiment_data.get('historical_avg_volume', 100)

            # Calculate volume factor (capped at 2x)
            volume_factor = min(current_volume / max(avg_volume, 1), self.config['volume_cap'])

            # Calculate cross-platform agreement
            platforms = sentiment_data.get('platforms', {})
            if len(platforms) > 1:
                sentiment_scores = [p.get('sentiment_score', 0) for p in platforms.values()]
                agreement = 1 - np.std(sentiment_scores) if sentiment_scores else 0.5
            else:
                agreement = 0.5

            # Calculate base shift
            base_shift = sentiment_delta * self.config['sentiment_multiplier']

            # Adjust by volume and agreement
            adjusted_shift = base_shift * volume_factor * agreement

            # Time horizon adjustment
            time_multipliers = {'1h': 0.5, '6h': 1.0, '24h': 1.5}
            time_multiplier = time_multipliers.get(time_horizon, 1.0)
            final_shift = adjusted_shift * time_multiplier

            # Calculate confidence
            confidence_score = min(volume_factor * agreement, 1.0)

            if confidence_score >= self.config['high_confidence_threshold']:
                confidence_level = 'high'
            elif confidence_score >= self.config['min_confidence_threshold']:
                confidence_level = 'medium'
            else:
                confidence_level = 'low'

            # Generate reasoning
            reasoning = self._generate_reasoning(
                sentiment_delta,
                volume_factor,
                agreement,
                current_volume,
                avg_volume
            )

            # Cap final shift to reasonable range (-20% to +20%)
            final_shift = max(-20.0, min(20.0, final_shift))

            return {
                'predicted_shift': round(final_shift, 2),
                'confidence_level': confidence_level,
                'confidence_score': round(confidence_score, 3),
                'reasoning': reasoning,
                'time_horizon': time_horizon,
                'created_at': datetime.utcnow(),
                'metadata': {
                    'sentiment_delta': round(sentiment_delta, 3),
                    'volume_factor': round(volume_factor, 2),
                    'agreement': round(agreement, 3),
                    'current_sentiment': round(current_sentiment, 3),
                    'previous_sentiment': round(previous_sentiment, 3)
                }
            }

        except Exception as e:
            logger.error(f"Error predicting market shift: {e}")
            return {
                'predicted_shift': 0.0,
                'confidence_level': 'low',
                'confidence_score': 0.0,
                'reasoning': 'Error in prediction calculation',
                'time_horizon': time_horizon,
                'created_at': datetime.utcnow()
            }

    def _generate_reasoning(
        self,
        sentiment_delta: float,
        volume_factor: float,
        agreement: float,
        current_volume: int,
        avg_volume: int
    ) -> str:
        """
        Generate human-readable reasoning for prediction.

        Args:
            sentiment_delta: Change in sentiment
            volume_factor: Volume multiplier
            agreement: Cross-platform agreement score
            current_volume: Current mention count
            avg_volume: Historical average volume

        Returns:
            Reasoning string
        """
        parts = []

        # Sentiment change
        if abs(sentiment_delta) > 0.1:
            direction = "increased" if sentiment_delta > 0 else "decreased"
            parts.append(f"Sentiment {direction} {abs(sentiment_delta):.2f}")
        else:
            parts.append("Sentiment relatively stable")

        # Volume
        if volume_factor > 1.5:
            parts.append(f"with {volume_factor:.1f}x higher volume ({current_volume} vs avg {avg_volume})")
        elif volume_factor > 1.0:
            parts.append(f"with {volume_factor:.1f}x volume")
        else:
            parts.append(f"with below-average volume")

        # Agreement
        if agreement > 0.7:
            parts.append(f"and strong cross-platform agreement ({agreement:.0%})")
        elif agreement > 0.4:
            parts.append(f"and moderate agreement ({agreement:.0%})")
        else:
            parts.append(f"but low cross-platform agreement ({agreement:.0%})")

        return " ".join(parts)

    def predict_multiple_markets(
        self,
        matched_data: List[Dict],
        time_horizons: List[str] = ['1h', '6h', '24h']
    ) -> List[Dict]:
        """
        Generate predictions for multiple matched markets.

        Args:
            matched_data: List of dicts with sentiment and market data
            time_horizons: List of time horizons to predict

        Returns:
            List of prediction dictionaries
        """
        predictions = []

        for data in matched_data:
            sentiment_data = data.get('sentiment', {})
            market_data = data.get('market', {})

            for horizon in time_horizons:
                prediction = self.predict_market_shift(
                    sentiment_data,
                    market_data,
                    time_horizon=horizon
                )
                prediction['market_id'] = market_data.get('market_id')
                prediction['market_title'] = market_data.get('title')
                prediction['current_probability'] = market_data.get('current_probability')
                predictions.append(prediction)

        return predictions

    def calculate_prediction_accuracy(
        self,
        prediction: Dict,
        actual_market_data: Dict
    ) -> Dict:
        """
        Calculate accuracy of a past prediction.

        Args:
            prediction: Original prediction dictionary
            actual_market_data: Current market data

        Returns:
            Accuracy metrics
        """
        try:
            predicted_shift = prediction.get('predicted_shift', 0)
            initial_prob = prediction.get('current_probability', 0.5)
            current_prob = actual_market_data.get('current_probability', 0.5)

            # Calculate actual shift
            actual_shift = (current_prob - initial_prob) * 100

            # Calculate error
            absolute_error = abs(predicted_shift - actual_shift)
            relative_error = absolute_error / max(abs(actual_shift), 0.01)

            # Direction accuracy
            predicted_direction = np.sign(predicted_shift)
            actual_direction = np.sign(actual_shift)
            direction_correct = (predicted_direction == actual_direction)

            return {
                'predicted_shift': predicted_shift,
                'actual_shift': round(actual_shift, 2),
                'absolute_error': round(absolute_error, 2),
                'relative_error': round(relative_error, 2),
                'direction_correct': direction_correct,
                'accuracy_score': round(max(0, 1 - relative_error), 3)
            }

        except Exception as e:
            logger.error(f"Error calculating accuracy: {e}")
            return {
                'error': str(e)
            }

    def get_signal_strength(self, prediction: Dict) -> str:
        """
        Categorize prediction signal strength.

        Args:
            prediction: Prediction dictionary

        Returns:
            Signal strength ('strong', 'moderate', 'weak')
        """
        confidence = prediction.get('confidence_score', 0)
        shift_magnitude = abs(prediction.get('predicted_shift', 0))

        if confidence >= 0.7 and shift_magnitude >= 5.0:
            return 'strong'
        elif confidence >= 0.4 and shift_magnitude >= 2.0:
            return 'moderate'
        else:
            return 'weak'


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test engine
    engine = PredictionEngine()

    # Sample sentiment data
    sentiment_data = {
        'current_score': 0.6,
        'previous_score': 0.2,
        'mention_count': 500,
        'historical_avg_volume': 200,
        'platforms': {
            'twitter': {'sentiment_score': 0.65},
            'reddit': {'sentiment_score': 0.55}
        }
    }

    # Sample market data
    market_data = {
        'market_id': 'BTC-100K-2026',
        'title': 'Will Bitcoin reach $100K?',
        'current_probability': 0.45
    }

    # Predict
    prediction = engine.predict_market_shift(sentiment_data, market_data, '6h')

    print(f"\nPrediction for: {market_data['title']}")
    print(f"Current probability: {market_data['current_probability']:.2%}")
    print(f"Predicted shift: {prediction['predicted_shift']:+.2f}%")
    print(f"Confidence: {prediction['confidence_level']}")
    print(f"Reasoning: {prediction['reasoning']}")

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK data (run once)
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_sentiment(text: str = None) -> dict:
    if text is None:
        text = "Donald trump is doing a poor job as the president of united states"
    
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    
    # Determine overall sentiment
    if sentiment_scores['compound'] >= 0.05:
        overall = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        overall = 'Negative'
    else:
        overall = 'Neutral'
    
    return {
        "scores": sentiment_scores,
        "overall_sentiment": overall,
        "text_analyzed": text
    } 

if __name__ == "__main__":
    # Example usage
    test_text = "donald trump is doing a poor job as the president of united states"
    result = analyze_sentiment(test_text)
    print("\nTest Results:")
    print(f"Text: {result['text_analyzed']}")
    print(f"Overall Sentiment: {result['overall_sentiment']}")
    print(f"Detailed Scores: {result['scores']}")

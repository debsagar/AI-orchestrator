from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import json
import sys

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_sentiment(text: str) -> dict:
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    
    if sentiment_scores['compound'] >= 0.05:
        overall = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        overall = 'Negative'
    else:
        overall = 'Neutral'
    
    return {
        "overall_sentiment": overall,
        "scores": sentiment_scores
    }

if __name__ == "__main__":
    # Read input from environment variable or command line
    input_text = sys.argv[1] if len(sys.argv) > 1 else "No text provided"
    result = analyze_sentiment(input_text)
    print(json.dumps(result))  # Output result as JSON 
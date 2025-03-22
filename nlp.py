from transformers import pipeline
from collections import deque
import datetime

ALERT_DAY_THRESHOLD = 1
ALERT_SECONDS_THRESHOLD = 600
ALERT_CONSECUTIVE_NEGATIVE_MSGS = 3
ALERT_DAY_NEGATIVE_MSGS = 5
NEGATIVE_SENTIMENT_THRESHOLD = 0.75

class SentimentTracker:
    def __init__(self):
        self.sentiments = deque(maxlen=20)  # recent messages with timestamps

    def record_sentiment(self, sentiment_score):
        now = datetime.datetime.now()
        self.sentiments.append((now, sentiment_score))

    def check_alert(self):
        recent = [(ts, s) for ts, s in self.sentiments if (datetime.datetime.now() - ts).days < ALERT_DAY_THRESHOLD]
        negative_msgs = [s for ts, s in recent if s >= NEGATIVE_SENTIMENT_THRESHOLD]

        if len(negative_msgs) >= ALERT_DAY_NEGATIVE_MSGS:
            return "ALERT_MANAGER"
        elif len(negative_msgs) >= ALERT_CONSECUTIVE_NEGATIVE_MSGS and all(
            (datetime.datetime.now() - ts).seconds < ALERT_SECONDS_THRESHOLD for ts, s in recent if s >= NEGATIVE_SENTIMENT_THRESHOLD):
            return "INTERNAL_REVIEW"
        else:
            return "NO_ACTION"


class SentimentAnalyzer:
    def __init__(self):
        self.pipeline = pipeline('sentiment-analysis',
                              model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                              top_k=None,
                              device="mps")

    def get_sentiment(self, msg):
        return next((item['score'] for item in self.pipeline(msg)[0] if item['label'] == 'negative'), None)


tracker = SentimentTracker()
analyzer = SentimentAnalyzer()

while True:
    negative_sentiment = analyzer.get_sentiment(input("Input: "))
    print(negative_sentiment)
    tracker.record_sentiment(negative_sentiment)
    print(tracker.check_alert())
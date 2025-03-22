from transformers import pipeline
from collections import defaultdict, deque
import datetime
import asyncio
from telegram import Bot


ALERT_DAY_THRESHOLD = 1
ALERT_SECONDS_THRESHOLD = 600
ALERT_CONSECUTIVE_NEGATIVE_MSGS = 3
ALERT_DAY_NEGATIVE_MSGS = 5
NEGATIVE_SENTIMENT_THRESHOLD = 0.75


BOT_TOKEN = "7798861328:AAETIEAFEvZclvvYbvEP3WC7y5HVkgKaolQ"
MANAGER_CHAT_ID = "557506446"
MANAGER_MAP = { # Example employees
    "emp001": 123456789,
    "emp002": 987654321,
}


async def send_alert_to_manager(manager_chat_id, employee_id):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=manager_chat_id,
        text=f"🚨 Sentiment Alert: Employee `{employee_id}` has shown repeated negative sentiment. Please check in.",
        parse_mode='Markdown'
    )


class SentimentTracker:
    def __init__(self):
        self.sentiments = deque(maxlen=20)

    def record_sentiment(self, sentiment_score):
        now = datetime.datetime.now()
        self.sentiments.append((now, sentiment_score))

    def check_alert(self):
        now = datetime.datetime.now()
        recent = [(ts, s) for ts, s in self.sentiments if (now - ts).days < ALERT_DAY_THRESHOLD]
        negative_msgs = [s for ts, s in recent if s >= NEGATIVE_SENTIMENT_THRESHOLD]

        if len(negative_msgs) >= ALERT_DAY_NEGATIVE_MSGS:
            return "ALERT_MANAGER"
        elif len(negative_msgs) >= ALERT_CONSECUTIVE_NEGATIVE_MSGS and all(
            (now - ts).seconds < ALERT_SECONDS_THRESHOLD for ts, s in recent if s >= NEGATIVE_SENTIMENT_THRESHOLD
        ):
            return "INTERNAL_REVIEW"
        else:
            return "NO_ACTION"


class SentimentAnalyzer:
    def __init__(self):
        self.pipeline = pipeline(
            'sentiment-analysis',
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            top_k=None,
            device="mps"
        )

    def get_sentiment(self, msg):
        result = self.pipeline(msg)[0]
        for item in result:
            if item['label'] == 'negative':
                return item['score']
        return 0.0


analyzer = SentimentAnalyzer()
employee_trackers = defaultdict(SentimentTracker)

print("💬 Start monitoring individual employee sentiment...\n")

while True:
    employee_id = input("Employee ID: ").strip()
    if employee_id not in MANAGER_MAP:
        print("⚠️ Unknown employee — skipping.\n")
        continue

    message = input("Message: ").strip()
    negative_score = analyzer.get_sentiment(message)
    print(f"Negative Score: {negative_score:.2f}")

    tracker = employee_trackers[employee_id]
    tracker.record_sentiment(negative_score)

    alert = tracker.check_alert()
    print(f"Status: {alert}\n")

    if alert == "ALERT_MANAGER":
        asyncio.run(send_alert_to_manager(MANAGER_CHAT_ID, employee_id))
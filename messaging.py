from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json
import os

BOT_TOKEN = "7798861328:AAETIEAFEvZclvvYbvEP3WC7y5HVkgKaolQ"
bot = Bot(token=BOT_TOKEN)
scheduler = BackgroundScheduler()

def send_contextual_prompt(context="early_phase", chat_id=None):
    messages = {
        "early_phase": "🧠 Reminder: Communicate the *why* behind this initiative clearly with your team today.",
        "mid_phase": "📊 Mid-phase prompt: Reinforce visible quick wins and acknowledge team progress.",
        "late_phase": "✅ End-phase reminder: Celebrate adoption wins and embed the change in team routines."
    }

    message = messages.get(context, "ℹ️ Default update for your change initiative.")
    bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

scheduler.add_job(lambda: send_contextual_prompt("early_phase"), 'cron', day_of_week='mon', hour=9)
scheduler.add_job(lambda: send_contextual_prompt("mid_phase"), 'cron', day_of_week='wed', hour=9)
scheduler.add_job(lambda: send_contextual_prompt("late_phase"), 'cron', day_of_week='fri', hour=9)
scheduler.start()

def save_user(chat_id, username, first_name):
    data = []
    file_path = "users.json"

    # Load existing users if file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

    # Check if user is already saved
    if not any(user["chat_id"] == chat_id for user in data):
        data.append({
            "chat_id": chat_id,
            "username": username,
            "first_name": first_name
        })
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ New user saved: {username or first_name} ({chat_id})")
    else:
        print(f"ℹ️ User {username or first_name} already exists.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['chat_id'] = update.effective_chat.id
    context.user_data['username'] = update.effective_user.username
    save_user(update.effective_chat.id, update.effective_user.username, update.effective_user.first_name)
    await update.message.reply_text("📥 You’re now subscribed to change management updates!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("✅ Bot is running. Press Ctrl+C to stop.")
app.run_polling()
import os
import json
import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# === CONFIGURATION ===
BOT_TOKEN = "7798861328:AAETIEAFEvZclvvYbvEP3WC7y5HVkgKaolQ"  # <-- 🔴 Replace with your actual token
USERS_FILE = "users.json"
FEEDBACK_FILE = "team_feedback.json"
bot = Bot(token=BOT_TOKEN)
scheduler = BackgroundScheduler()

# === PROMPT DEFINITIONS ===
PROMPTS = {
    "awareness": "📢 *Awareness Phase*: Remind your team *why* this change matters. Connect it to their daily challenges.",
    "adoption": "🛠️ *Adoption Phase*: Help your team take their first steps. Normalize the learning curve. Offer support.",
    "momentum": "🚀 *Momentum Phase*: Share wins. Reinforce visible progress. Celebrate efforts.",
    "sustain": "📘 *Sustain Phase*: Embed the new normal. Ask what habits or tools should be locked in.",
    "default": "ℹ️ Default update: Keep supporting your team through this change!"
}

# === UTILITIES: Load / Save ===
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = []

    # Ensure all users have required fields
    for user in users:
        user.setdefault("update_score", 0)
        user.setdefault("phase", "awareness")
        user.setdefault("team_id", f"team_{user['chat_id']}")
    return users

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def save_user(chat_id, username, first_name):
    users = load_users()
    if not any(u["chat_id"] == chat_id for u in users):
        users.append({
            "chat_id": chat_id,
            "username": username,
            "first_name": first_name,
            "team_id": f"team_{chat_id}",
            "phase": "awareness",
            "update_score": 0
        })
        save_users(users)

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return {}

def calculate_score(sentiment_list):
    score = 0
    for item in sentiment_list:
        if item["sentiment"] == "positive":
            score += 2
        elif item["sentiment"] == "negative":
            score -= 2
    return score

# === ASYNC SCHEDULED PROMPT JOB ===
async def update_scores_and_send_prompts():
    users = load_users()
    feedback = load_feedback()

    for user in users:
        team_id = user["team_id"]
        sentiments = feedback.get(team_id, [])
        delta = calculate_score(sentiments)
        user["update_score"] += delta

        phase = user["phase"]
        prompt = PROMPTS.get(phase, PROMPTS["default"])
        score_msg = f"\n\n📊 *Update Score*: {user['update_score']} (Change this week: {delta:+})"

        await bot.send_message(chat_id=user["chat_id"], text=prompt + score_msg, parse_mode='Markdown')

    save_users(users)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump({}, f)

def scheduled_job():
    asyncio.run(update_scores_and_send_prompts())

# === TELEGRAM COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    save_user(chat_id, username, first_name)

    await update.message.reply_text(
        "📥 You’re now subscribed to change management updates!\n"
        "Your team's current phase is set to *awareness*.\n"
        "Use /setphase to change it, or /prompt to get your current tip.",
        parse_mode='Markdown'
    )

async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users = load_users()
    for user in users:
        if user["chat_id"] == chat_id:
            phase = user["phase"]
            score = user["update_score"]
            message = PROMPTS.get(phase, PROMPTS["default"])
            await update.message.reply_text(
                f"📬 *Prompt for phase: {phase}*\n\n{message}\n\n📊 *Update Score*: {score}",
                parse_mode='Markdown'
            )
            return
    await update.message.reply_text("❌ You are not registered. Use /start to subscribe.")

async def setphase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    valid_phases = ["awareness", "adoption", "momentum", "sustain"]
    if not context.args:
        await update.message.reply_text("ℹ️ Usage: /setphase awareness | adoption | momentum | sustain")
        return

    new_phase = context.args[0].lower()
    if new_phase not in valid_phases:
        await update.message.reply_text("❌ Invalid phase. Choose: awareness, adoption, momentum, sustain.")
        return

    chat_id = update.effective_chat.id
    users = load_users()
    for user in users:
        if user["chat_id"] == chat_id:
            user["phase"] = new_phase
            save_users(users)
            await update.message.reply_text(
                f"✅ Your team's phase has been set to *{new_phase}*.",
                parse_mode='Markdown'
            )
            return
    await update.message.reply_text("❌ You are not registered. Use /start to subscribe.")

# === MAIN BOT LAUNCH ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prompt", prompt))
    app.add_handler(CommandHandler("setphase", setphase))

    scheduler.add_job(scheduled_job, 'cron', day_of_week='mon,wed,fri', hour=9)
    scheduler.start()

    print("✅ Bot is running. Press Ctrl+C to stop.")
    app.run_polling()
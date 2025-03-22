from botbuilder.core import TurnContext, MessageFactory, BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
import asyncio

APP_ID = 'MICROSOFT_APP_ID'
APP_PASSWORD = 'MICROSOFT_APP_PASSWORD'
SERVICE_URL = 'https://smba.trafficmanager.net/emea/'
CONVERSATION_ID = 'TEAMS_CONVERSATION_ID'

settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

async def send_proactive_message(adapter, conversation_reference):
    async def proactive_message(turn_context: TurnContext):
        await turn_context.send_activity(
            "Reminder: Communicate the 'why' behind today's AI rollout clearly to your team."
        )

    await adapter.continue_conversation(
        conversation_reference=conversation_reference,
        callback=proactive_message,
        bot_id=APP_ID
    )

if __name__ == "__main__":
    asyncio.run(send_proactive_message())
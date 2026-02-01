import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
# This sample slack application uses SocketMode
# For the companion getting started setup guide,
# see: https://docs.slack.dev/tools/bolt-python/getting-started


# find_dotenv() automatically locates the file in the project root
# load_dotenv() reads it and puts it into os.environ
load_dotenv(find_dotenv())

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)
MODEL_NAME = "upstage/solar-pro-3:free"




# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!.......Write Bot <Your Message> to inovke AI"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Hit API"},
                    "action_id": "button_click",
                },
            }
        ]
        # ,
        # text=f"Hey there <@{message['user']}>!....Write Bot to inovke AI",
    )
# Let us try to add some AI capabilites

@app.message("bot")
def interact_ai(message,say):
    full_text = message.get("text")
    print(f"Received: {full_text}")

    # Temporary "Thinking" message
    temp_msg = say(f"🧠 Thinking using {MODEL_NAME}...")

    try:
        # 3. The Call (Standard OpenAI Format)
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful coding assistant. Keep answers concise and limit it to 2 to 3 lines only unless it is the ask of any script or code"
                },
                {
                    "role": "user",
                    "content": full_text
                }
            ],
            
        )

        # 4. Extract Answer
        answer = completion.choices[0].message.content
        
        print(f"✅ Response received ({len(answer)} chars)")
        say(answer)

    except Exception as e:
        print(f"❌ Error: {e}")
        say(f"⚠️ OpenRouter Error: {e}")




@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()










# print("Fetching available models for provided api key...")
# try:
#     for m in client.models.list():
#         # UPDATE: Check 'supported_actions' instead of 'supported_generation_methods'
#         if "generateContent" in (m.supported_actions or []):
#             print(f"- {m.name}")
            
# except Exception as e:
#     print(f"Error: {e}")
"""
東吳大學資料系 2025 LINEBOT
"""

import os

from flask import Flask, abort, request
from bs4 import BeautifulSoup
import markdown

from google import genai
from google.genai import types # 加入system prompot所需的types模組

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent


# Initialize Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)
chat = client.chats.create(model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="你是一個中文的AI助手，請用繁體中文回答"    
    )
)

# Initialize Flask app
app = Flask(__name__)
channel_secret = os.getenv("YOUR_CHANNEL_SECRET")
channel_access_token = os.getenv("YOUR_CHANNEL_ACCESS_TOKEN")
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


def query(payload: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    response = chat.send_message(message=payload)
    return response.text


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return {"message": "Line Webhook Server"}


@app.route("/", methods=["POST"])
def callback():
    """Handle incoming webhook from LINE."""
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    app.logger.info("Request body: %s", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.warning(
            "Invalid signature. Please check channel credentials."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    """Handle incoming text message event."""
    user_input = event.message.text.strip()
    response_text = query(user_input)
    html_msg = markdown.markdown(response_text)
    soup = BeautifulSoup(html_msg, "html.parser")

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=soup.get_text())],
            )
        )
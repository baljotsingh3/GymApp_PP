# your_app/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

from Member.utils.llm import LLMService
from asgiref.sync import sync_to_async



import logging
logger = logging.getLogger(__name__)



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info("WebSocket connection established.")
        await self.accept()
        
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get('message', '')

        llm = LLMService()
        result = await sync_to_async(llm.send_query)(user_message)

        ai_message = result['response'] if result['success'] else 'AI service error.'

        await self.send(text_data=json.dumps({
            'message': ai_message
        }))

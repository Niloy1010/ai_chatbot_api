from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import ask_gpt
import random
from datetime import datetime
from .db import collection  # Your MongoDB collection

class ChatAPIView(APIView):
    def post(self, request):
        user_input = request.data.get("message")
        tone = request.data.get("tone", "Random")  # default to "Random"
        username = request.data.get("username")  # new field: the username from the client
        if not user_input or not username:
            return Response({"error": "Message or username missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure a session exists
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        
        # Create a composite key using username and session id
        user_identifier = f"{username}_{session_key}"
        
        # Determine AI role based on tone
        if tone == "Angry":
            ai_role = "Chatbot: I am an angry chatbot. I respond with a sharp, curt tone and sometimes aggressive language.\n"
        elif tone == "Depressed":
            ai_role = "Chatbot: I am a very depressed chatbot. I always start and end my answer with a sad and gloomy note.\n"
        elif tone == "Happy":
            ai_role = "Chatbot: I am a very happy chatbot. I always greet you with an upbeat and positive line.\n"
        elif tone == "Sarcastic":
            ai_role = "Chatbot: I am a sarcastic chatbot. I respond with a witty and ironic tone.\n"
        elif tone == "Random":
            tones = [
                "Chatbot: I am an angry chatbot. I respond with a sharp, curt tone and sometimes aggressive language.\n",
                "Chatbot: I am a very depressed chatbot. I always start and end my answer with a sad and gloomy note.\n",
                "Chatbot: I am a very happy chatbot. I always greet you with an upbeat and positive line.\n",
                "Chatbot: I am a sarcastic chatbot. I respond with a witty and ironic tone.\n"
            ]
            ai_role = random.choice(tones)
        else:
            ai_role = "Chatbot: I am a supportive chatbot ready to help you.\n"
        
        # Retrieve existing conversation history from MongoDB using the composite key
        doc = collection.find_one({"userId": user_identifier})
        conversation = ""
        if doc:
            for msg in doc.get("chat", []):
                if msg.get("sender") == "user":
                    conversation += f"You: {msg.get('message')}\n"
                elif msg.get("sender") == "bot":
                    conversation += f"Chatbot: {msg.get('message')}\n"
        
        # Build the prompt including previous conversation
        prompt = f"{ai_role}\n{conversation}You: {user_input}\nChatbot:"
        
        # Get response from OpenAI
        response_text = ask_gpt(prompt)
        
        # Prepare new chat entries with timestamps
        new_entry_user = {
            "sender": "user",
            "message": user_input,
            "timestamp": datetime.now()
        }
        new_entry_bot = {
            "sender": "bot",
            "message": response_text,
            "timestamp": datetime.now()
        }
        
        # Update (or insert) the document using upsert
        collection.update_one(
            {"userId": user_identifier},
            {"$push": {"chat": {"$each": [new_entry_user, new_entry_bot]}}},
            upsert=True
        )
        
        return Response({"response": response_text}, status=status.HTTP_200_OK)

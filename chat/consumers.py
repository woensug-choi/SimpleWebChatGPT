import json
import uuid  # Import uuid module
import asyncio, datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.sessions.backends.db import SessionStore

from . import tasks

import openai, os
# Set OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Define a function to ask questions to OpenAI GPT
def ask_gpt(prompt, session_id):
    response = openai.Completion.create(
        model=os.environ['OPENAI_MODEL'],
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        user=session_id,
    )
    message = response.choices[0].text
    return message.strip()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Create a new session and retrieve the session ID
        session = SessionStore()
        session.create()
        self.session_id = session.session_key

        # Initialize the chat history
        self.chat_history = "" 

        # Accept the WebSocket connection
        self.accept()

    def disconnect(self, close_code):
        # Close the session when the WebSocket connection is closed
        SessionStore(session_key=self.session_id).delete()

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        prompt = text_data_json['message']
        if prompt:
            # Log input
            self.chat_history += f"HUMAN: {prompt}\n"
            
            # Send prompt to Websocket immediately
            self.chat_prompt(prompt)

            response = self.ask_gpt_stream(self.chat_history \
                + "\n\nAct as a ChatGPT-3 chat bot who can respond faster and pretend smarter than HUMAN. In the chat history above, AI is you. Don't add 'AI:' in the responses and answer the last question." \
                + " Answer the last HUMAN's question in the context of the convrsation history. And response in the same language as the last question." \
                + os.environ['PROMPT_OPTION']  \
                + "\n\n", self.session_id)

            # Update the conversation history
            self.chat_history += f"AI: {response}\n"

            # print(self.chat_history)
            # Log the response to a file
            if not os.path.isfile('chat.log'):
                open('chat.log', 'w+').close()
            with open('chat.log', "a") as file:
                file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                + "\nfrom " + self.scope["client"][0] + "\n" + prompt + "\n" + response + "\n\n")
            # Save only prompts
            if not os.path.isfile('prompts.csv'):
                open('prompts.csv', 'w+').close()
            with open('prompts.csv', "a") as file:
                file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                + "," + self.scope["client"][0] + "," + prompt)


        # Handle incoming messages
        pass
    
    def ask_gpt_stream(self, prompt, session_id):
        current_time = datetime.datetime.now()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            user=session_id,
            stream=True,
        )

        compelete = ""

        # iterate through the stream of events
        for event in response:
            event_text = event['choices'][0]['text']  # extract the text
            self.chat_partial(event_text, current_time)
            compelete += event_text
        
        # Print empty lines
        # self.chat_emptylines()
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat_message',
                'prompt': None,
                'response': '\n',
            }
        )
        
        return compelete

    # Send prompt to WebSocket
    def chat_prompt(self, prompt):
        self.send(text_data=json.dumps({
            'prompt': f"{prompt}"
        }))

    # Send partial responses to WebSocket
    def chat_partial(self, partial, current_time):
        self.send(text_data=json.dumps({
            'partial': f"{partial}",
            'time': f"{current_time}"
        }))

    # Send response to WebSocket
    def chat_message(self, event):
        response = event['response']
        self.send(text_data=json.dumps({
            'response': f"{response}"
        }))

    # Send response to WebSocket
    def chat_emptylines(self):
        self.send(text_data=json.dumps({
            'response': f"\n\n"
        }))

            



import os
from dotenv import load_dotenv
from google import genai

# lê o arquivo .env e o deixa disponível no sistema 
load_dotenv()

# lê o valor da variável de ambiente
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def resposta_ia(prompt):

    client = genai.Client(api_key=GOOGLE_API_KEY)
    modelo = "gemini-2.5-flash"

    chat = client.chats.create(model= modelo)
    resposta = chat.send_message(prompt)

    return resposta.text
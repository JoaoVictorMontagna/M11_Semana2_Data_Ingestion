import os
from dotenv import load_dotenv


load_dotenv()

# Configurações
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

print(RABBITMQ_HOST,RABBITMQ_QUEUE,SUPABASE_URL,SUPABASE_API_KEY)


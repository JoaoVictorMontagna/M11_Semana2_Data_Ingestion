import pika
import json
import os
import time
import random
from faker import Faker
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configurações do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

# Inicializar Faker para gerar dados aleatórios
faker = Faker()

# Lista de fontes simuladas
FONTES = ["fonte_1", "fonte_2", "fonte_3", "fonte_4"]

def gerar_dado():
    """Gera um JSON com dados aleatórios e identifica a fonte."""
    return {
        "id": faker.uuid4(),
        "nome": faker.name(),
        "idade": random.randint(18, 70),
        "cidade": faker.city(),
        "email": faker.email(),
        "telefone": faker.phone_number(),
        "data_cadastro": faker.date_time_this_decade().isoformat(),
        "fonte": random.choice(FONTES)  # Adiciona a informação da fonte
    }

def enviar_dado():
    """Envia mensagens aleatórias para o RabbitMQ com delay."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    while True:
        dado = gerar_dado()
        mensagem = json.dumps(dado)
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=mensagem)

        print(f"Mensagem enviada: {mensagem}")

        # Adicionar um delay aleatório entre 1 e 5 segundos
        delay = random.randint(1, 5)
        print(f"Aguardando {delay} segundos antes do próximo envio...")
        time.sleep(delay)

if __name__ == "__main__":
    enviar_dado()

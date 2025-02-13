import pika
import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis do .env
load_dotenv()

# Configurações do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Criar cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def callback(ch, method, properties, body):
    """Processa mensagens do RabbitMQ e insere nas tabelas bronze e prata do Supabase."""
    try:
        # Decodificar a mensagem recebida
        dados = json.loads(body.decode())
        print(f"Mensagem recebida: {dados}")

        # Inserir na tabela Bronze (raw_data)
        # A coluna 'created_at' é preenchida automaticamente no banco
        bronze_payload = {"raw_data": dados}
        response_bronze = supabase.table("bronze").insert(bronze_payload).execute()
        print(f"Inserido em bronze: {response_bronze.data}")

        # Inserir na tabela Prata (raw_data + tag)
        # O campo 'tag' indicará de qual fonte a mensagem veio (campo 'fonte' no JSON)
        prata_payload = {
            "raw_data": dados,
            "tag": dados.get("fonte", "desconhecida")
        }
        response_prata = supabase.table("prata").insert(prata_payload).execute()
        print(f"Inserido em prata: {response_prata.data}")

    except Exception as e:
        print(f"Erro ao processar/inserir mensagem: {e}")

def iniciar_consumidor():
    """Inicia o consumidor do RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

    print("Aguardando mensagens na fila...")
    channel.start_consuming()

if __name__ == "__main__":
    iniciar_consumidor()

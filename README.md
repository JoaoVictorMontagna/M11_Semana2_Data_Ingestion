
# Documentação de Configuração e Execução

## Pré-requisitos
- Docker e Docker Compose instalados
- Poetry instalado

---

## Passo 1 – Configurar o Ambiente
1. Clone ou copie o projeto.
2. Instale as dependências:
   ```bash
   poetry install
   ```

---

## Passo 2 – Configurar e Iniciar o RabbitMQ
1. Crie o arquivo `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     rabbitmq:
       image: rabbitmq:3-management
       container_name: rabbitmq
       ports:
         - "5672:5672"
         - "15672:15672"
   ```

2. Suba o RabbitMQ:
   ```bash
   docker-compose up -d
   ```

3. Verifique se está rodando:
   ```bash
   docker ps | grep rabbitmq
   ```

4. Acesse o painel RabbitMQ:
   - URL: `http://localhost:15672`
   - Login: `guest` | Senha: `guest`

---

## Passo 3 – Executar Producer e Consumer
1. Abra dois terminais.
2. No primeiro terminal, execute o consumer:
   ```bash
   poetry run python consumer.py
   ```
3. No segundo terminal, execute o producer:
   ```bash
   poetry run python producer.py
   ```

---

## Passo 4 – Parar os Serviços
1. Pare o RabbitMQ:
   ```bash
   docker-compose down
   ```

---

## Observações
- O nome do container é definido como `rabbitmq` para evitar nomes aleatórios.
- Verifique o estado do Docker caso ele não abra corretamente:
   - Finalize os processos no Gerenciador de Tarefas e reinicie.
   - Limpe containers e redes corrompidas:
     ```bash
     docker system prune -a
     ```

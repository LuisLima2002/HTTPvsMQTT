import requests
import psutil
import paho.mqtt.client as mqtt
import time
from datetime import datetime

# Configurações do broker MQTT
broker_address = "127.0.0.1"
client_id = "publisher"  # ID do cliente MQTT

# Cria o cliente MQTT e se conecta ao broker
client = mqtt.Client(client_id=client_id)
client.connect(broker_address)

# Loop infinito para enviar o uso da memória RAM a cada 5 segundos
while True:
    # Obtém o uso atual da memória RAM em bytes
    mem = psutil.virtual_memory().used
    
    # Converte para megabytes e arredonda para 2 casas decimais
    mem = round(mem / 1024 / 1024, 2)
    
    # Publica o uso da memória RAM no tópico "mem/usage"
    topic = "mem/usage17"
    message = str(mem) + " MB"
    message = str("lastChange at ")+ datetime.now().strftime("%H:%M:%S") +" <br> value "+ message
    client.publish(topic, message)
    requests.post("http://localhost:8080/saveMemUsage",data={"usage":message})
    # Espera 5 segundos antes de enviar o próximo uso da memória RAM
    time.sleep(5)



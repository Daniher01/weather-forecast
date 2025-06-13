import os
from twilio.rest import Client
import time
import pandas as pd
import requests
import boto3

# Cliente SNS
sns_client = boto3.client('sns')

def get_forecast(response, i):
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return fecha, hora, condicion, tempe, rain, prob_rain

# ← CAMBIO: Función SNS en lugar de Twilio
def send_message_sns(message):
    topic_arn = os.environ['SNS_TOPIC_ARN']
    
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='🌧️ Alerta Lluvia Málaga'
    )
    
    return response

def lambda_handler(event, context):
    # ✅ MOVER TODO AQUÍ DENTRO
    query = 'Málaga'
    api_key = os.environ['API_KEY_WAPI']
    url_clima = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1&aqi=no&alerts=no'
    
    try:
        # ✅ CON TIMEOUT Y MANEJO DE ERRORES
        response = requests.get(url_clima, timeout=5).json()
    except requests.RequestException as e:
        print(f"Error al consultar API del clima: {e}")
        return {
            'statusCode': 500,
            'body': f'Error al consultar clima: {str(e)}'
        }
    
    datos = []
    
    for i in range(len(response['forecast']['forecastday'][0]['hour'])):
        datos.append(get_forecast(response, i))
    
    col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']
    df = pd.DataFrame(datos, columns=col)
    
    # Filtrar cuando llueve
    df_rain = df[(df['Lluvia'] == 1) & (df['Hora'] > 6) & (df['Hora'] < 22)]
    df_rain = df_rain[['Hora', 'Condicion']]
    df_rain.set_index('Hora', inplace=True)
    
    template = f'{str(df_rain)}'
    
    try:
        time.sleep(1)  # ✅ Reducir de 2 a 1 segundo
        message = send_message_sns(template)
        
        return {
            'statusCode': 200,
            'body': f'Mensaje enviado: {message.sid}'
        }
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        return {
            'statusCode': 500,
            'body': f'Error al enviar mensaje: {str(e)}'
        }
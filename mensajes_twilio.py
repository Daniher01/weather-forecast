import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI
import time 

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import pandas as pd 
import requests 
from bs4 import BeautifulSoup 
from tqdm import tqdm 

from datetime import datetime 

# ? Armado de la URL

query = 'Málaga'
api_key = API_KEY_WAPI

url_clima = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1&aqi=no&alerts=no'

response = requests.get(url_clima).json() 

def get_forecast(response,i):
    
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain =response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return fecha,hora,condicion,tempe,rain,prob_rain

datos = []

# tqdm permite visualizar una barra de carga en los ciclos for
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])), colour = 'green'): 
    datos.append(get_forecast(response,i))
    
col = ['Fecha','Hora','Condicion','Temperatura','Lluvia', 'prob_lluvia']
df = pd.DataFrame(datos,columns=col)


# filtrar cuando llueve
df_rain = df[(df['Lluvia']==1) & (df['Hora']>6) & (df['Hora'] < 22)]
df_rain = df_rain[['Hora', 'Condicion']]
df_rain.set_index('Hora', inplace = True)

template = f'{str(df_rain)}'


time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages.create(
    body=template,
    from_=PHONE_NUMBER,
    to="+34744786798",
)

print(f'Mensaje Enviado {message.sid}')
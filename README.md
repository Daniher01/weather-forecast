# 🌦️ Weather Forecast SMS Bot

Un sistema automatizado que envía pronósticos del tiempo por SMS desde una instancia EC2 de AWS.

## 📋 Descripción del Proyecto

Este proyecto es un bot automatizado que consulta el clima de Málaga, España y envía notificaciones SMS cuando detecta probabilidad de lluvia durante el día. El sistema se ejecuta de forma programada en la nube de AWS, proporcionando alertas meteorológicas útiles de manera completamente automática.

## 🛠️ Tecnologías Utilizadas

### APIs y Servicios en la Nube
- **AWS EC2** - Instancia en la nube donde se ejecuta el bot automáticamente
- **Twilio API** - Plataforma de comunicaciones para el envío de mensajes SMS
- **WeatherAPI** - Servicio que proporciona datos meteorológicos actualizados y pronósticos

### Desarrollo
- **Python 3.11** - Lenguaje de programación principal
- **pipenv** - Gestión de dependencias y entornos virtuales
- **pandas** - Procesamiento y análisis de los datos meteorológicos
- **requests** - Comunicación con las APIs externas
- **Ubuntu** - Sistema operativo de la instancia EC2

## ⚡ Funcionamiento

1. **Obtención de Datos**: El bot consulta WeatherAPI para obtener el pronóstico horario de Málaga
2. **Procesamiento**: Analiza los datos y filtra únicamente las horas con probabilidad de lluvia durante el día (7 AM - 10 PM)
3. **Notificación**: Si detecta lluvia, formatea la información y envía un SMS a través de Twilio
4. **Automatización**: Todo el proceso se ejecuta automáticamente mediante tareas programadas en la instancia EC2

## 📊 Características

- **Filtrado Inteligente**: Solo notifica cuando realmente hay probabilidad de lluvia
- **Información Precisa**: Muestra las horas específicas y el tipo de condición meteorológica
- **Ejecución Automática**: Funciona sin intervención manual desde la nube
- **Enfoque Local**: Configurado específicamente para Málaga, Andalucía

## 🌐 Infraestructura

El proyecto está desplegado en **AWS EC2**, aprovechando la confiabilidad y disponibilidad de la nube de Amazon para asegurar que las notificaciones se envíen de manera consistente y oportuna.

## 📁 Estructura del Proyecto

```
weather-forecast/
├── mensajes_twilio.py          # Script principal del bot
├── mensajes_twilio.ipynb       # Notebook de desarrollo y pruebas
├── twilio_config.py           # Configuraciones de APIs
├── Pipfile                    # Dependencias del proyecto
└── archivos de configuración y logs
```

---
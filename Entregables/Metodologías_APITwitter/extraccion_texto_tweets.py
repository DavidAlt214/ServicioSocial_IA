import tweepy
import csv

# credenciales de Twitter
consumer_key = 'Agg5IStnnShqYaoJN6biAeBQu'
consumer_secret = '2P7lNSvSscTGJvxK5DdCtdV1CVTkOXTPOzcdGK2iMJRSa5Gh9q'
access_token = '1262305256-8ctdDA5S1lweILT0SWMLQucqyNwifXSYsccGk0R'
access_token_secret = 'AcxYvNAd5mmNl7nj5q9pObDzZKEWkeoYe4gGAGTwq9rpM'

#Autenticación con la API de Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Archivo de entrada CSV con enlaces de tweets generados
archivo_csv_entrada = 'output4.csv'

# Archivo de salida CSV con información adicional (por ejemplo, texto del tweet)
archivo_csv_salida = 'tweets_con_texto.csv'

# Crear una lista para almacenar la información de salida
tweets_con_texto = []

# Leer el archivo CSV de entrada
with open(archivo_csv_entrada, 'r', encoding='utf-8') as archivo_entrada:
    csv_reader = csv.reader(archivo_entrada)
    next(csv_reader)  # Saltar la fila de encabezados

    for row in csv_reader:
        tweet_id, geo_source, country, state, county, city, tweet_link = row

        # Obtener el ID del tweet desde el enlace
        tweet_id_str = tweet_link.split('/')[-1]

        try:
            # Obtener el texto del tweet utilizando la API de Twitter
            tweet = api.get_status(tweet_id_str, tweet_mode='extended')
            tweet_text = tweet.full_text
        except tweepy.TweepyException as e:
            # Manejar el caso de errores al obtener el tweet
            if isinstance(e, tweepy.Forbidden):
                tweet_text = f'Error 403 Forbidden: No tienes acceso a este tweet'
            else:
                tweet_text = f'Error al obtener el tweet: {str(e)}'

        # Agregar la información al resultado
        tweets_con_texto.append([tweet_id, geo_source, country, state, county, city, tweet_link, tweet_text])

# Escribir la información de salida en un nuevo archivo CSV
with open(archivo_csv_salida, 'w', newline='', encoding='utf-8') as archivo_salida:
    csv_writer = csv.writer(archivo_salida)
    
    # Encabezados para el archivo CSV de salida
    encabezados = ['Tweet ID', 'Geo Source', 'País', 'Estado', 'Condado', 'Ciudad', 'Tweet Link', 'Texto del Tweet']
    csv_writer.writerow(encabezados)

    # Escribir las filas en el archivo CSV de salida
    csv_writer.writerows(tweets_con_texto)

print(f"La información de texto de tweets ha sido guardada en {archivo_csv_salida}")

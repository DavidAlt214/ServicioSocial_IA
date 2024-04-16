import pandas as pd
import tweepy

# Configura las credenciales de la API de Twitter (v2)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAA2msgEAAAAAxnqmE9wVnDzgu5DN5CWj2W6ftOc%3DJVNh6ofiQmEoh0fu3rMmFj0BFIpOYWqibYTitkkB6GMIJgIGxn'

# Configura la autenticación con Tweepy (v2)
auth = tweepy.Client(bearer_token=bearer_token)

# Archivo de entrada CSV con enlaces de tweets generados
archivo_csv_entrada = 'output4.csv'

# Archivo de salida CSV con información adicional (por ejemplo, texto del tweet)
archivo_csv_salida = 'tweets_text_prueba.csv'

# Crea una lista para almacenar los textos de los tweets
tweets_text = []

# Lee el archivo CSV con pandas, especificando el tipo de datos
df = pd.read_csv(archivo_csv_entrada, dtype=str)

# Encuentra la columna que contiene los tweet_id
tweet_id_column = None
for column in df.columns:
    if 'tweet_id' in column.lower():
        tweet_id_column = column
        break

if tweet_id_column is None:
    raise ValueError("No se encontró una columna que contenga 'tweet_id' en el nombre.")

# Itera sobre las filas del DataFrame
for index, row in df.iterrows():
    tweet_id = row[tweet_id_column]
    tweet_url = row['tweet_url']

    # Usa Tweepy para obtener el texto del tweet (v2)
    try:
        tweet = auth.get_tweet(id=tweet_id, tweet_fields=["text"])
        tweet_text = tweet['text']
        tweets_text.append(tweet_text)
    except tweepy.TweepError as e:
        # Maneja errores de la API de Twitter
        print(f"Error al obtener el tweet {tweet_id}: {e}")
        tweets_text.append('Error al obtener el tweet')

# Crea un nuevo DataFrame con los textos de los tweets
df_text = pd.DataFrame({tweet_id_column: df[tweet_id_column], 'tweet_text': tweets_text})

# Guarda el nuevo DataFrame en un archivo CSV
df_text.to_csv(archivo_csv_salida, index=False)

print(f"La información de texto de tweets ha sido guardada en {archivo_csv_salida}")

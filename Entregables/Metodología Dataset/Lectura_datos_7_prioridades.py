import json
import csv

archivo_principal = 'locations-01Febrero.json'
limite_archivos = 666575
archivos_procesados = 0
archivo_csv = 'output4.csv'

def generate_tweet_link(user_id, tweet_id):
    # Verificar si hay un user_id antes de generar el enlace
    if user_id:
        return f'https://twitter.com/{user_id}/status/{tweet_id}'
    return f'https://twitter.com/status/{tweet_id}'

def geo_source_priority(geo_source):
    # Asignar prioridades a las fuentes de geo
    priorities = {'coordinates': 0, 'place': 1, 'user_location': 2, 'tweet_text': 3}
    return priorities.get(geo_source, float('inf'))

with open(archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
    csv_writer = csv.writer(archivo_csv)

    # Encabezados para el archivo CSV
    encabezados = ['Tweet ID', 'Geo Source', 'País', 'Estado', 'Condado', 'Ciudad', 'Tweet Link']
    csv_writer.writerow(encabezados)

    filas = []

    with open(archivo_principal, 'r') as archivo_principal:
        for linea in archivo_principal:
            try:
                datos = json.loads(linea)
                user_id = datos.get('user_id', '')
                tweet_id = datos['tweet_id']
                geo_source = datos.get('geo_source', '')

                fila = [tweet_id, geo_source]

                if geo_source == 'coordinates':
                    # Tomar la información de las coordenadas
                    geo = datos.get('geo', {})
                    fila.extend([
                        geo.get('country_code', ''),
                        geo.get('state', ''),
                        geo.get('county', ''),
                        geo.get('city', ''),
                    ])
                elif geo_source == 'place':
                    # Tomar la información de place
                    place = datos.get('place', {})
                    fila.extend([
                        place.get('country_code', ''),
                        place.get('state', ''),
                        place.get('county', ''),
                        place.get('city', ''),
                    ])
                elif geo_source == 'user_location':
                    user_location = datos.get('user_location', {})
                    fila.extend([
                        user_location.get('country_code', ''),
                        user_location.get('state', ''),
                        user_location.get('county', ''),
                        user_location.get('city', ''),
                    ])
                elif geo_source == 'tweet_text':
                    # Tomar la información de tweet_locations
                    tweet_locations = datos.get('tweet_locations', [{}])[0]
                    fila.extend([
                        tweet_locations.get('country_code', ''),
                        tweet_locations.get('state', ''),
                        tweet_locations.get('county', ''),
                        tweet_locations.get('city', ''),
                    ])
                else:
                    # Manejar otros casos, si es necesario
                    fila.extend([''] * 4)

                tweet_link = generate_tweet_link(user_id, tweet_id)
                fila.append(tweet_link)

                filas.append(fila)
                archivos_procesados += 1

                if archivos_procesados >= limite_archivos:
                    break

            except json.decoder.JSONDecodeError as e:
                print(f"Error al decodificar JSON en la línea {archivos_procesados + 1}: {e}")

    # Ordenar las filas por prioridad de geo_source
    filas_ordenadas = sorted(filas, key=lambda x: geo_source_priority(x[1]))

    # Escribir las filas ordenadas al archivo CSV
    csv_writer.writerows(filas_ordenadas)

print(f"La información ha sido guardada y ordenada por prioridades en {archivo_csv}")

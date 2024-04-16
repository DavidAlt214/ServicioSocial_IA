import os
import pandas as pd

def generate_tweet_link(user_id, tweet_id):
    return f"https://twitter.com/{user_id}/status/{tweet_id}"

def merge_csv_files(folder_path, output_file):
    # Lista de nombres de archivos CSV en la carpeta
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Inicializar una lista para almacenar los datos combinados
    combined_data = []

    # Iterar sobre cada archivo CSV
    for file in csv_files:
        # Leer el archivo CSV
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, dtype=str)  # Leer el archivo CSV tratando todas las columnas como cadenas de texto

        # Extraer las columnas requeridas
        user_ids = df['data.search_by_raw_query.search_timeline.timeline.instructions.entries.content.itemContent.tweet_results.result.legacy.user_id_str']
        tweet_ids = df['data.search_by_raw_query.search_timeline.timeline.instructions.entries.content.itemContent.tweet_results.result.rest_id']
        texts = df['data.search_by_raw_query.search_timeline.timeline.instructions.entries.content.itemContent.tweet_results.result.legacy.full_text']
        locations = df['data.search_by_raw_query.search_timeline.timeline.instructions.entries.content.itemContent.tweet_results.result.core.user_results.result.legacy.location']

        # Combinar los datos en una lista de tuplas
        combined_data.extend(zip(user_ids, tweet_ids, texts, locations))

    # Crear un DataFrame con los datos combinados
    combined_df = pd.DataFrame(combined_data, columns=['User_ID', 'Tweet_ID', 'Texto', 'Ubicación'])

    # Generar los enlaces para cada tweet
    combined_df['Enlace del Tweet Original'] = combined_df.apply(lambda row: generate_tweet_link(row['User_ID'], row['Tweet_ID']), axis=1)

    # Guardar el DataFrame combinado en un nuevo archivo CSV
    combined_df.to_csv(output_file, index=False)
    print(f"Datos combinados guardados en {output_file}")

# Carpeta que contiene los archivos CSV
folder_path = "Textos tweets Dashboard"

# Nombre del archivo de salida
output_file = "datos_combinados.csv"

# Llamar a la función para combinar los archivos CSV
merge_csv_files(folder_path, output_file)

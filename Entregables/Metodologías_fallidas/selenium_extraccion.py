from twitter_scraper_selenium import scrape_keyword
import pandas as pd
import json

def scrape_tweets_from_links(links_file):
    # Leer los enlaces de tweets del archivo CSV generado
    df = pd.read_csv(links_file)
    tweet_links = df['Tweet Link'].tolist()

    # Scrapear los tweets para cada enlace
    all_tweets = []
    for link in tweet_links:
        tweets = scrape_keyword(
            headless=True,
            keyword=link,
            browser="chrome",
            tweets_count=1,  # Solo el tweet específico
            output_format="csv"
        )
        # Leer los tweets desde el archivo CSV
        tweets_df = pd.read_csv(tweets)
        # Convertir a formato JSON y agregar a la lista de tweets
        tweets_json = json.loads(tweets_df.to_json(orient='records'))
        all_tweets.extend(tweets_json)

    return all_tweets

# Uso del código
links_file = 'output4.csv'
tweets = scrape_tweets_from_links(links_file)
print(tweets)

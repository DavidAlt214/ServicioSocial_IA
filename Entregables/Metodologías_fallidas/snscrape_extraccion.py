import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "covid-19 (#covid)"
tweets = []
limit = 10


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
    # print(vars(tweet))
    # break
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.username, tweet.content])
        
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
print(df)

#Twitter ha bloqueado snscrape de la extracción de datos 

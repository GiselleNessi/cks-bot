from dotenv import load_dotenv
import tweepy
import schedule
import time
import os
import random

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Check if any of the API credentials are missing
if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
    raise ValueError("One or more Twitter API credentials are missing. Please check your .env file.")
else:
    print("Twitter API credentials found.")

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)
print("Twitter client initialized.")

educational_phrases = [
    "Blockchain permite transacciones seguras y transparentes sin necesidad de intermediarios. 🌐💳",
    "Los contratos inteligentes en blockchain automatizan acuerdos sin la necesidad de intermediarios. 🤖📜",
    "La descentralización en blockchain brinda mayor seguridad y resistencia a la censura. 🔒🌐",
    "Bitcoin es la primera y más conocida aplicación de la tecnología blockchain. 🚀🔗",
    "Blockchain puede revolucionar la industria financiera al proporcionar transacciones eficientes y seguras. 💸🌐",
    "Las criptomonedas utilizan tecnología blockchain para garantizar la integridad de las transacciones. 💎🔗"
]

posted_phrases_file = "posted_phrases.txt"

def read_posted_phrases():
    try:
        with open(posted_phrases_file, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def write_posted_phrase(phrase):
    with open(posted_phrases_file, "a") as file:
        file.write(phrase + "\n")

def post_educational_tweet():
    posted_phrases = read_posted_phrases()
    remaining_phrases = list(set(educational_phrases) - set(posted_phrases))

    if not remaining_phrases:
        print("All phrases have been posted. Resetting...")
        write_posted_phrase("")  # Reset the posted phrases

    educational_phrase = random.choice(remaining_phrases)

    try:
        response = client.create_tweet(
            text=educational_phrase
        )
        print(f"Educational tweet posted successfully! Tweet URL: https://twitter.com/user/status/{response.data['id']}")
        write_posted_phrase(educational_phrase)
    except tweepy.errors.Forbidden as e:
        print(f"An error occurred: {e}")
    except tweepy.errors.TooManyRequests as e:
        print(f"Rate limit exceeded. Waiting and retrying...")
        time.sleep(60)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Schedule the educational tweet to run every hour
schedule.every().hour.do(post_educational_tweet)
print("Educational tweet scheduler set up.")

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
    print("Script is running...")

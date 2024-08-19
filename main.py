from atproto import Client
from subprocess import call
from datetime import datetime
from grammar import Grammar
import os, shutil

import tweepy
import sys

try:
    import settings
except ImportError:
    print("Could not import settings module, did you create one?")
    exit()

try:
    from gpio_watcher import GPIOWatcher
except ImportError:
    print("Import GPIOWatcher failed, the script will only work in test mode.")


def goGoPaparazzo():
    
    # get a pretty date time string 
    timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

    hour = datetime.now().hour
    #if hour < 8 or hour > 17:
    #    print "Yawn, I'm asleep. Wake me up when it's daytime"
    #    return
    
    print(f"Activating Paparazzo at {timestamp}")
    
    grammar = Grammar.from_file("grammar.txt")
    while True:
        message = grammar.generate()
        if len(message) < 252: # allow space for picture URL
            break
    print(f"Message: {message}")
    
    # capture image to capture.jpg
    call(["./capture-image.sh"], shell=True)
    
    # stop here if image capture failed
    if not os.path.exists("capture.jpg"):
        print("Error - no capture.jpg recorded")
        return

    if settings.post_twitter == True:
        # post to twitter
        twitter2 = tweepy.Client(
            consumer_key = settings.app_key,
            consumer_secret = settings.app_secret,
            access_token = settings.oauth_token,
            access_token_secret = settings.oauth_token_secret
        )

        auth = tweepy.OAuth1UserHandler(
            consumer_key = settings.app_key,
            consumer_secret = settings.app_secret,
            access_token = settings.oauth_token,
            access_token_secret = settings.oauth_token_secret
        )

        twitter1 = tweepy.API(auth)
        media = twitter1.media_upload("capture.jpg")
        twitter2.create_tweet(text=message, media_ids = [ media.media_id_string ])

        print("Posted to Twitter.")

    if settings.post_bluesky == True:
        # post to bluesky
        client = Client(base_url="https://bsky.social")
        client.login(settings.bluesky_user, settings.bluesky_pass)

        with open("capture.jpg", "rb") as c:
            img_data = c.read()

        client.send_image(
            text = message,
            image = img_data,
            image_alt = "Daphne the cat using her internet connected catflap."
        )

        print("Posted to Bluesky.")
 
    # archive the image and text
    shutil.move("capture.jpg", "history/%s.jpg" % timestamp)
    with open("history/%s.txt" % timestamp, "w") as f:
        f.write("%s\n" % message)
    


if __name__ == "__main__":
    if "--test" in sys.argv:
        goGoPaparazzo()
    else:
        watcher = GPIOWatcher(7, onChange=goGoPaparazzo, debounceSeconds=20)
        while True:
            try:
                watcher.enter_loop()
            except Exception as e:
                print(f"Error: {e}")

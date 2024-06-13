from twython import Twython
import argparse

parser = argparse.ArgumentParser("twitter_auth")
parser.add_argument("--key", help="Your app API key from Twitter.", required=True)
parser.add_argument("--secret", help="Your app API secret from Twitter.", required=True)
args = parser.parse_args()

twitter = Twython(args.key, args.secret)
auth = twitter.get_authentication_tokens()
print(auth)

f = open("settings.py", "w")
f.write(f"app_key=\"{args.key}\"\n")
f.write(f"app_secret=\"{args.secret}\"\n")
f.write(f"oauth_token=\"{auth['oauth_token']}\"\n")
f.write(f"oauth_token_secret=\"{auth['oauth_token_secret']}\"\n")
f.close()

print("Created settings.py")
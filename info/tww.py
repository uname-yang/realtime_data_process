#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "851652975957127168-kCdHaLXCHAf3yBzynoKc62jG7fxI71O"
access_token_secret = "iV330tl5xRtN960uXHHyImcTwBlt5CYSqwb7EH4EJcCWy"
consumer_key = "PRUgkvxvKCAvfT6cnoG8ZueMg"
consumer_secret = "WwtS8oKDT3H7dqQxNdQ7idUk5gMYX1ZeWXDA199QOHKLWIQhoQ"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])

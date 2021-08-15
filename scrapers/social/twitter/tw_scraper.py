from typing import Dict, List
from logging import info, exception
from twitter import Api, TwitterError

from config import (
    TW_CONSUMER_KEY,
    TW_CONSUMER_SECRET,
    TW_ACCESS_TOKEN_KEY,
    TW_ACCESS_TOKEN_SECRET
)


class TwScraper(object):
    def __init__(self):
        self.api = None

        self.consumer_key = TW_CONSUMER_KEY
        self.consumer_secret_key = TW_CONSUMER_SECRET
        self.access_token_key = TW_ACCESS_TOKEN_KEY
        self.access_token_secret_key = TW_ACCESS_TOKEN_SECRET

        self.parsed_data = {}

    def __init_tw_api(self) -> Api or None:
        try:
            api = Api(
                self.consumer_key,
                self.consumer_secret_key,
                self.access_token_key,
                self.access_token_secret_key
            )
        except TwitterError as e:
            exception(msg=f'[-]\tFailed to initialize twitter api: {e.message}')
            return None

        return api

    def __get_tweets(self, screen_name=None) -> List[super]:
        timeline = self.api.GetUserTimeline(screen_name=screen_name, count=200)
        earliest_tweet = min(timeline, key=lambda x: x.id).id

        while True:
            tweets = self.api.GetUserTimeline(
                screen_name=screen_name, max_id=earliest_tweet, count=200
            )
            new_earliest = min(tweets, key=lambda x: x.id).id

            if not tweets or new_earliest == earliest_tweet:
                break
            else:
                earliest_tweet = new_earliest
                print("getting tweets before:", earliest_tweet)
                timeline += tweets

        return timeline

    def get_parsed_data(self) -> Dict[str, str]:
        return self.parsed_data

    def scrape(self, user: str) -> None:
        info(msg='[*]\tStarting the twitter scraping process...', level=0)

        self.api = self.__init_tw_api()

        if self.api is None:
            return

        # user            = self.api.GetUser()
        # friends         = self.api.GetFriends()
        # followers       = self.api.GetFollowers()
        # followers_ids   = self.api.GetFollowerIDs()
        # retweeters      = self.api.GetRetweeters()
        # retweets        = self.api.GetUserRetweets()
        # replies         = self.api.GetReplies()
        # favorites       = self.api.GetFavorites()
        # timeline        = self.__get_tweets(screen_name=user)

        # self.parsed_data = user
        # self.parsed_data.update({
        #     'friends'   : friends,
        #     'followers' : followers_ids,
        #     'retweets'  : retweets,
        #     'replies'   : replies,
        #     'favorites' : favorites
        # })

        info(msg='[+] The scraping twitter has been done!', level=0)

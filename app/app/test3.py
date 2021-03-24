# import os
# import tweepy
# import random

# from services.word import WordService


# auth = tweepy.OAuthHandler(
#     os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
# auth.set_access_token(os.environ['ACCESS_TOKEN'],
#                       os.environ['ACCESS_TOKEN_SECRET'])

# api = tweepy.API(auth)


# NEGATIVE_WORD_LIST = (
#     "死",
#     "ﾀﾋ",
#     "タヒ",
#     "他界",
#     "亡く",
#     "成仏",
#     "逝去",
#     "老衰",
#     "絶命",
#     "不幸",
#     "先立",
#     "訃報"
#     "冥福"
#     "遺体"
#     "葬",
#     "殺",
#     "命の火",
#     "息の根",
#     "息を引",
#     "がん",
#     "末期",
#     "病",
#     "犯",
#     "罪",
#     "薬",
#     "違法",
#     "違反",
#     "逮捕",
#     "鬱",
#     "うつ",
#     "苦",
#     "暴",
#     "殴",
#     "痛",
#     "絶望",
# )

# # api.update_status("投稿テスト")

# # public_tweets = api.home_timeline()
# # for tweet in public_tweets:
# #     print('-------------------------')
# #     print(tweet.text)


# # public_tweets = api.home_timeline()
# # for tweet in public_tweets:
# #     print('-------------------------')
# #     print(tweet.text)


# # for tweet in tweepy.Cursor(api.search, q='むーちゃん').items(10):
# #     # print(tweet)
# #     print(tweet.text)

# # class MyTweet:
# #     __init__


# class TweetService:

#     def post_tweet(self, msg):
#         """ ツイートする
#         """
#         api.update_status(msg)

#     def trend_tweet(self):
#         """ ツイッタートレンドからランダムでピックアップしてツイートする
#         """
#         # 日本のWOEID
#         woeid = 23424856
#         # トレンド取得
#         trends = api.trends_place(woeid)[0]
#         # トレンドワードからランダムで取得
#         trend_word = random.choice(trends["trends"])["name"]

#         #
#         topic = "(仮)"
#         msg = "最近「{}」って言葉をよく耳にするよ！\nでも、むーちゃんは何の事かよく分かんない。\nだれか教えにきて欲しいな！\nhttps://torichan.app".format(
#             trend_word, topic)
#         # ツイートする
#         self.post_tweet(msg)

#     def ng_word_check(self, word, limit):
#         """ 指定したワードが不適切な単語かチェックする
#             wordで検索したツイート20件の中にNGワードが一定数含まれているかチェック
#             limitで指定した数ヒットしたらTrueを返す
#         """
#         ng_word_hit = 0
#         for tweet in tweepy.Cursor(api.search, q=word, result_type="popular").items(20):
#             for ng_word in NEGATIVE_WORD_LIST:
#                 if ng_word in tweet.text:
#                     ng_word_hit = ng_word_hit + 1
#                     break
            
#             if ng_word_hit >= limit:
#                 return True

#         return False

#     def remembered_tweet(self, word):
#         """ 覚えたワードについてツイートする
#         """

#     def known_word_tweet(self):
#         """ 知っているワードについてツイートする
#         """

#     def unknown_word_tweet(self):
#         """ 意味を知らないワードについてツイートする
#         """


# tweet_saervice = TweetService()
# # tweet_saervice.trend_tweet()
# print( tweet_saervice.ng_word_check("喧嘩", 3) )

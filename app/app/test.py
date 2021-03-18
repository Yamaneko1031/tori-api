# from google.cloud import firestore

# db = firestore.Client()

# # docs = db.collection(u'words').where(u'tag_list', u'array_contains', u'便利').stream()
# docs = db.collection(u'words').where(u'tag_list', u'array_contains', u'難しい').get()
# # docs = db.collection(u'words').where(u'tag_list', u'in', [[u'便利']]).stream()

# for doc in docs:
#     print(doc.to_dict()['word'])


import MeCab

tagger = MeCab.Tagger(
    '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
# tagger = MeCab.Tagger('')
# text = "ゲームとか映画やアニメになっている鬼滅の刃は東京の西の方にある地域。高速に計算をすることが出来る機械"
# text = "牧場物語おもしろい。トマトが美味しそう。とうもろこしとかたけのこも出て来る。宝石とかも。"
text = "ピカチュウとリラックマ、デデンネ、ドラえもん、ねこっぱち"
result = tagger.parse(text)
print(result)



def analysis(word):
    node = tagger.parseToNode(word)
    phraseCnt = 0
    result = {}
    kind = ""

    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            phraseCnt += 1
            part = node.feature.split(",")
            kind = "名詞：一般"
            
            if (part[0] == "名詞"):
                if(part[1] == "固有名詞"):
                    if(part[2] == "一般"):
                        kind = "名詞：一般"
                    elif(part[2] == "人名"):
                        kind = "名詞：人名"
                    elif(part[2] == "地域"):
                        if(part[3] == "国"):
                            kind = "名詞：国"
                        elif(part[3] == "一般"):
                            kind = "名詞：一般"
                        elif(part[3] == "組織"):
                            kind = "名詞：一般"
                        
                if(part[1] == "一般"):
                    kind = "名詞：一般"

            if (part[0] == "形容詞"):
                if(part[1] == "自立"):
                    kind = "形容詞"

    if( phraseCnt > 1):
        kind = "不明"

    result["kind"] = kind
    result["phrase"] = phraseCnt



# node = tagger.parseToNode(text)
# partCnt = 0
# while node:
#     if node.surface != "":  # ヘッダとフッタを除外
#         partCnt += 1
#         part = node.feature.split(",")
        
#         if (part[0] == "名詞"):
#             if(part[1] == "固有名詞"):
#                 if(part[2] == "一般"):
#                 elif(part[2] == "人名"):
#                 elif(part[2] == "地域"):
#                     elif(part[3] == "国"):
#                     elif(part[3] == "一般"):
#                     elif(part[3] == "組織"):
                    
#             if(part[1] == "一般"):


#         if (part[0] == "形容詞"):
#             if(part[1] == "自立"):









#         if (part[0] == "名詞"):
#             if(part[1] == "一般" or part[1] == "固有名詞"):
#                 print("{}って何？".format(node.surface))
#             elif(part[1] == "サ変接続"):
#                 print("僕も{}できるよ！！".format(node.surface))
#                 print("むーちゃんは{}苦手かもしれないなー".format(node.surface))
#         elif (part[0] == "形容詞"):
#             print(node.surface)

#     node = node.next

# print("単語数:{}".format(partCnt))

# while node:
#     if node.surface != "":  # ヘッダとフッタを除外
#         part = node.feature.split(",")
#         if (part[0] == "名詞"):
#             if(part[1] == "一般" or part[1] == "固有名詞"):
#                 print(node.surface)
#         elif (part[0] == "形容詞"):
#             print(node.surface)

#     node = node.next

# -Oyomi (ヨミ付与)
# -Ochasen (ChaSen互換)
# -Odump (全情報を出力)

# import os
# import tweepy

# auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
# auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

# api = tweepy.API(auth)

# api.update_status("投稿テスト")

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print('-------------------------')
#     print(tweet.text)
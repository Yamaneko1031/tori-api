import MeCab

tagger = MeCab.Tagger(
    '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')

def disassemble(text):
    node = tagger.parseToNode(text)
    phraseCnt = 0
    kind = ""
    phraseList = {}

    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            phraseCnt += 1
            part = node.feature.split(",")
            kind = ""
            word = node.surface

            if (part[0] == "名詞"):
                if(part[1] == "一般"):
                    kind = "名詞：一般"
                elif(part[1] == "サ変接続"):
                    kind = "名詞：サ変接続"
                elif(part[1] == "形容動詞語幹"):
                    kind = "形容動詞"
                elif(part[1] == "固有名詞"):
                    if(part[2] == "一般"):
                        kind = "名詞：一般"
                    elif(part[2] == "人名"):
                        # kind = "名詞：人名"
                        pass
                    elif(part[2] == "地域"):
                        if(part[3] == "国"):
                            kind = "名詞：国"
                        elif(part[3] == "組織"):
                            # kind = "名詞：一般"
                            pass
                        else:
                            # kind = "名詞：地域"
                            pass

            elif (part[0] == "形容詞"):
                if(part[1] == "自立"):
                    kind = "形容詞"
                    word = part[6]

            if(kind != ""):
                phraseList[word] = kind
                # phraseList.append({"word": node.surface, "kind": kind})

        node = node.next

    return phraseList
# create_dict.py에서 만든 단어 사전 테스트
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Utils.Preprocess import Preprocess
import pickle

#단어 사전 불러오기
f = open("./chatbot_dict.bin", "rb")
word_index = pickle.load(f)
f.close()

text = '안녕하세요. 테스트 코드입니다. 단어사전 만들기 성공!'

#전처리 객체 생성
p=Preprocess(userdic='./Utils/user_dic.tsv')

#형태소 분석기 실행
pos = p.pos(text)
print(pos)

#품사 태그 없이 키워드 출력
keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
    try:
        print(word, word_index[word])
    except KeyError:
        #해당 단어가 없는 경우 oov 처리
        print(word, word_index['OOV'])
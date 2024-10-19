#2번
#챗봇에서 사용하는 단어 사전 생성 하기

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle
import pandas as pd

#말뭉치 데이터 읽어오기
movie_review = pd.read_csv('./데이터/data_to_csv/네이버.csv') # 네이버 영화 리뷰
purpose =pd.read_csv('./데이터/data_to_csv/용도별목적대화데이터.csv') # 용도별목적대화데이터
topic = pd.read_csv('./데이터/data_to_csv/주제별일상대화데이터.csv') # 주제별일상대화데이터
coomon_sense = pd.read_csv('./데이터/data_to_csv/일반상식.csv') # 일반상식

#결측치 제거 
movie_review.dropna(inplace=True)
purpose.dropna(inplace=True)
topic.dropna(inplace=True)
coomon_sense.dropna(inplace=True)

#각 컬럼명이 document, text, query + answer에 있는 문장들을 리스트로 만듦
text1 = list(movie_review['document']) #네이버영화 
text2 = list(purpose['text']) #용도별목적대화데이터
text3 = list(topic['text']) #주제별일상대화데이터
text4 = list(coomon_sense['query']) + list(coomon_sense['answer']) #일반상식

#리스트 다 더하기
corpus_data = text1 + text2 + text3 + text4 

#말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성 - 1
p= Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c) #형태소분석기
    for k in pos:
        dict.append(k[0])

#사전에 사용될 word2index 생성 - 2
#사전의 첫 번째 인덱스에는 oov 사용
#OOV 토큰을 추가해 단어 사전 외의 단어가 입력될 경우 OOV토큰으로 처리하도록 함
#단어 사전에 포함되는 단어의 수를 가장 많이 등장하는 10만개의 단어로 지정함
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV', num_words = 100000)
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index

#사전 파일 생성 - 3
f = open("chatbot_dict.bin", "wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()

# - 1
#읽어온 말뭉치 데이터 리스트에서 문장을 하나씩 불러와 pos(형태소와 품사 태그 추출)태깅함
#형태소 분석 결과를 단어 리스트에 저장함

# - 2
# 토크나이저를 이용해 1에서 만들어진 단어 리스트를 단어 인덱스 딕셔너리(word_index) 데이터로 만듦

# - 3
#생성된 단어 인덱스 딕셔너리(word_index) 객체 파일로 저장함
#그럼 chatbot 메인 경로에 chatbot_dict.bin 파일 생성됨

#단어 사전 구축이유
#입력받은 텍스트를 pos태깅과 불용어 처리 과정을 거친 후 
#컴퓨터가 텍스트를 처리하기 위해서 토크나이징된 텍스트에 대해 숫자로 바꿔주는 처리가 필요함
#이렇게 단어 임베딩을하는 과정에서 단어를 어떤 숫자로 바꿔줄지에 대한 단어 사전을 구축해야함
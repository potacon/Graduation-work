#최종 7번
#챗봇 엔진 서버

import threading
import json
import pandas as pd
import tensorflow as tf
import torch

from Utils.BotServer import BotServer
from Utils.Preprocess import Preprocess
from Utils.FindAnswer import FindAnswer
from Models.intent.IntentModel import IntentModel
from Train_tools.qna.create_embedding_data import create_embedding_data


#텐서플로우 gpu 메모리 할당 - 추가 1
#tf는 시작시 메모리를 최대로 할당하기 때문에 0번 gpu를 4gb메모리만 사용하도록 설정함
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        tf.config.experimental.set_virtual_device_configuration(gpus[0],
                        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
    except RuntimeError as e:
        print(e)
#즉 위 코드는 0번 gpu를 사용하며, 4GB의 메모리 할당을 하겠다고 정의함

#로그 기능 - 추가 2
from logging import handlers
import logging

#log settings
LogFormatter = logging.Formatter('%(asctime)s,%(message)s')

#handler settings
LogHandler = handlers.TimedRotatingFileHandler(filename='./logs/chatbot.log', when='midnight', interval=1, encoding='utf-8')
LogHandler.setFormatter(LogFormatter)
LogHandler.suffix = "%Y%m%d"

#logger set
#실제 사용할 logger를 생성, 출력 레벨을 ERROR 이상으로 설정, handler 추가
Logger = logging.getLogger()
Logger.setLevel(logging.ERROR)
Logger.addHandler(LogHandler)




#전처리 객체 생성
p = Preprocess(word2index_idc= './chatbot_dict.bin')
print('텍스트 전처리기 로드 완료')

# 의도 파악 모델
intent = IntentModel(model_name='./intent_model.h5', preprocess=p)
print('의도 파악 모델 로드 완료')

#엑셀 파일 로드
df = pd.read_excel('./Train_tools/qna/train_data.xlsx')
print('엑셀 파일 로드 완료')
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

#pt 파일 갱신 및 불러오기
create_embedding_data = create_embedding_data(df = df, preprocess=p)
create_embedding_data.create_pt_file()
embedding_data = torch.load('./Train_tools/qna/embedding_data.pt')
print('임베딩 pt 파일 갱신 및 로드 완료')

# - 1
def to_client(conn, addr):
    try:
        #데이터 수신 - 1.1
        read= conn.recv(2048) #수신 데이터가 있을 때까지 블로킹
        print('==================')
        print('Connection from %s' % str(addr))

        if read is None or not read:
            #클라이언트 연결이 끊어지거나 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0) #스레드 강제 종료
        
        #json 데이터로 변환 - 1.2
        recv_json_data = json.loads(read.decode())
        print('데이터 수신: ', recv_json_data)
        query = recv_json_data['Query']

        #의도 파악 - 1.3
        intent_pred = intent.predict_class(query)
        intent_name = intent.labels[intent_pred]
        print('의도파악 완료')

        #답변 검색 - 1.4
        f = FindAnswer(df = df, embedding_data=embedding_data, preprocess=p)
        selected_qes, score, answer, imageUrl, query_intent  = f.search(query, intent_name)
        print('답변 검색 완료')
        print('score: {}'.format(score))

        #로그 기능 - 추가 2
        if score < 0.60:
            answer = "부정확한 질문이거나 잘모르겠습니다."
            imageUrl = "nan"
            #사용자 질문, 예측 의도, 선택된 질문, 유사도 점수
            Logger.error(f"{query},{intent_name},{selected_qes},{query_intent},{score}")


        # - 1.5
        send_json_data_str = {
            "Query" : selected_qes,
            "Answer": answer,
            "imageUrl" : imageUrl,
            "Intent": intent_name
        }
        message = json.dumps(send_json_data_str) #json객체 문자열로 변환
        conn.send(message.encode()) #응답 전송
        print('응답전송 완료')

    except Exception as ex:
        print('오류')
        print(ex)

if __name__ == '__main__':
    #봇 서버 동작 - 2
    port = 5050
    listen = 1000
    bot = BotServer(port, listen)
    bot.create_sock()
    print('bot start')

    while True:
        conn, addr = bot.ready_for_client()
        client = threading.Thread(target=to_client, args=(
            conn, #클라이언트 연결 소켓
            addr, #클라이언트 연결 주소 정보
        ))
        client.start()

# -1
#to_client()함수는 client의 server연결 수락되는 순간 실행되는 스레드 함수
#챗봇 클라이언트에서 질의한 내용을 처리해 적절한 답변을 찾은 후 다시 챗봇 클라이언트에 응답을 전송
#챗봇 엔진의 처리 과정이 함수 내부에 구현되어있음 

#먼저 client로부터 데이터를 받기 위해 대기하는 부분
# 데이터수신 - 1.1
#이 객체를 통해 클라이언트와 데이터를 주고받음
#recv()메서드는 데이터가 수신될 때까지 블로킹 된다.
#최대 2048바이트만큼 데이터를 수신함
#클라이언트와의 연결이 끊어지거나 오류가 있는 경우에는 블로킹이 해제되어 None이 반환됨 

# json 데이터로 변환 - 1.2
#챗봇 클라이언트로부터 수신된 데이터를 JSON 객체로 변환하는 부분
#이때 json 포맷은 앞서 정의한 챗봇 클라이언트에서 server쪽으로 요청하는 json 프로토콜이다.

#의도 파악 - 1.3
#챗봇 클라이언트로부터 수신된 질문 텍스트의 의도를 파악함

#답변 검색 - 1.4
#분석된 의도를 이용해 답변을 검색함

# - 1.5
#검색된 답변 데이터(의도, 답변 텍스트, 이미지 url)를 앞서 정의한 서버에서 client쪽으로 응답하는 json 포맷으로 객체로 생성함
#소켓 통신으로는 객체 형태로 데이터 송신이 불가능
#따라서 json.dump()함수를 통해 json 객체를 문자열로 변환함


#봇 서버 동작 - 2
#챗봇 서버 소켓을 생성함
#챗봇 엔진 서버의 통신 port=5050, 최대 client 연결 수는 1000으로 설정함
#챗봇 엔진 서버 동작 이후 챗봇 클라이언트는 서버 ip와 서버에서 설정한 port가 오픈되어 있어야 접속 가능

#while 무한루프를 돌면서 client 연결을 기다림
#client의 server 연결 요청이 server에서 수락되는 즉시 챗봇 클라이언트의 서비스 요청을 처리할 수 있는 스레드를 생성함
#이때 생성되는 스레드는 to_client()함수를 호출함


#################################################################

#추가 로그기능 - 2
# logging.Formatter는 
#로그 생성의 형식을 결정
#%(asctime)s: 로그가 기록되는 시간
#%(message)s: 로그 메시지

# handlers.TimedRotatingFileHandler
#로그 파일을 생성하는 기준
#filename: 파일이름
#when='midnight' 매일 자정을 기준으로 새로운 파일을 생성
#suffix 기준으로 파일 생성

#구현한 로그 기능은 유사도 점수가 0.6보다 작으면 
#사용자 질문, 예측 의도, 선택된 질문, 선택된 질문 의도, 유사도 점수의 내용을 기록하도록 구현함
#그래서 FindAnswer.py내용도 변경해야함
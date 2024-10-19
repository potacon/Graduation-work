#챗봇 rest api 서버 구현
from flask import Flask, request, jsonify, abort, render_template
import socket
import json

#챗봇 엔진 서버 정보 - 1
host="127.0.0.1" #챗봇 엔진 서버 ip 주소
port = 5050 #챗봇 엔진 서버 통신 포트

#flask 애플리케이션
app = Flask(__name__)

#챗봇 엔진 서버와 통신 - 2
def get_answer_form_engine(bottype, query):
    #챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host,port))

    #챗봇 엔진 질의 요청 2.1
    json_data = {
        'Query': query,
        'BotType':bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    #챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    #챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data

#챗봇 엔진 query 전송 api - 3
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == 'NORMAL':
            #일반 질의응답 api
            ret = get_answer_form_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)
        else:
            #정의되지 않은 bot type인 경우 404 error
            abort(404)
    except Exception as ex:
        #오류 발생시 500 error
        abort(500)

#시작 문구 추가
@app.route('/hello', methods=['GET'])
def index():
    try:
        message = '안녕하세요 인제대학교 컴퓨터공학과 챗봇서비스 입니다.'
        json_data = {
            'message' : message
        }
        message = json.dumps(json_data, ensure_ascii=False)
        message = json.loads(message)
        print(message)
        
        return jsonify(message)
    except Exception as ex:
        #오류 발생시 500 error
        abort(500)


@app.route('/data')
def get_data():
    data = {'name': 'John', 'age': 30}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

#챗봇 엔진 서버 정보 - 1
#챗봇 엔진 서버(main/chatbot.py) 접속에 필요한 host port 변수에 저장

#챗봇 엔진 서버와 통신 - 2
#get_answer_form_engine() 함수는 챗봇 엔진 서버에 소켓 통신으로 질의를 전송함
#서버로부터 성공적으로 답변 데이터를 수신한 경우 응답으로 받은 json 문자열을 딕셔너리 객체로 반환함

#챗봇 엔진 질의 요청 2.1 
#입력 받은 질문 텍스트를 사전에 약속한 프로토콜 포맷으로 JSON 객체를 생성한 뒤 데이터 전송이 가능한 문자열 형태로 변환
#이후 utf8로 인코딩하고 챗봇 엔진 server에 문자열 데이터를 전송함

#챗봇 엔진 query 전송 api - 3
#<bot_type> 동적 변수에는 api를 호출하는 메신저 플랫폼 명칭이 할당되어 있다.
#여기서 명칭은 NORMAL로 사용
#body = request.get_json() 함수를 통해 post / query/<bot_type> api 요청 시 body에 담긴 json 데이터를 딕셔너리 형태로 가져옴
#get_answer_form_engine()함수를 사용해 챗봇 엔진 서버로부터 답변을 받아옴


#정리
#get_answer_form_engine() 함수는 챗봇 엔진 서버에 소켓 통신으로 질문을 전달하고,
#다시 답변 데이터를 받아오는 함수.

#api를 통해 post 방식으로 /query/NORMAL url를 통해 json 객체의 전달을 주고 받을 수 있음
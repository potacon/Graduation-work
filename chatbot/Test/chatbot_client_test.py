import socket
import json

#챗봇 엔진 서버 접속 정보 - 1
host = "127.0.0.1" #챗봇 엔진 서버 ip 주소
port=5050 #챗봇 엔진 서버 통신 포트

#클라이언트 프로그램 시작 - 2
while True:
    print('질문: ') 
    query = input() #질문 입력 - 2.1
    if(query == 'exit'):
        exit(0)
    print('-'*40)

    #챗봇 엔진 서버 연결 - 2.2
    mySocket = socket.socket()
    mySocket.connect((host, port))

    #챗봇 엔진 질의 요청 - 2.3
    josn_data = {
        'Query' : query,
        'BotType' : "TEST"
    }
    message = json.dumps(josn_data)
    mySocket.send(message.encode())

    #챗봇 엔진 답변 출력 - 2.4
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    print('답변: ')
    print(ret_data['Answer'])
    print(ret_data)
    print(type(ret_data))
    print('\n')

    #챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()
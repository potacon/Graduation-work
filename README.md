# 졸작

이 프로젝트는 제가 학업 과정에서 배운 주요 개념, 도구 및 방법을 보여주기 위해 고안되었습니다. 아래에서는 프로젝트 목적, 설정 지침 및 기여 방법에 대한 개요를 확인할 수 있습니다.<br>

## 프로젝트 개요

이 프로젝트에서는 [ 머신러닝, 자연어 처리, 이미지 분류, 챗봇 ] 에 초점을 맞춘 최종 프로젝트 입니다.<br>
프로젝트의 목표는 학과 학생들이 사용하기 쉬운 학과 전용 챗봇 ai 제작 입니다.

## 특징

## 사용된 기술

* 프로그래밍 언어 : python, JavaScript, CSS, HTML
* 프레임워크/라이브러리 : Tensorflow, Pytorch, flask(server)
* 도구 : git, VSCode
* 모델 : KR-SBERT( Embedding model )


## 프로젝트 실행되는 순서 

문장이 들어오면 <br>

1. 전처리( 형태소, 품사 태거 / 불용어 제거 )
2. 문장 embedding ( 전처리 된 문장 tensor화 )
3. cosine similarity를 이용하여 질문 답변 엑셀에서 ' 질문 데이터 선택 '
4. 선택된 질문에서 의도를 번호로 판단 ( 0 : default , 1 : 장소, 2 : 시간 )
5. 최종적으로 선택된 질문 문장을 인코딩하여 'similarity 점수 측정 '
6. similarity 점수가 가장 높은 답변 출력

### 추가 문제 1 
- 유사도를 비교하는 과정에서 SBERT 모델을 사용하며 pytorch를 이용하는데 만약 cpu가 아닌 gpu 사용시 메모리 부족 현상이 발생할 가능성이 있음
- 추가로 gpu 메모리 할당이 필요한 경우(서버 환경에서 다른 프로그램을 상시 실행하는 겨우)등 여러 상황에 대비해 적절한 메모리의 할당이 필요함

### 해결 
- main chatbot.py(챗봇 서버)에 텐서플로우 메모리할당 코드 작성

### 추가 문제 2
- 만약 답변이 없는 질문이나 의도 모델에 관한 질문이 들어오면 성능 개선이 필요하다

### 해결 

- 로그 기능을 추가한다.
- 로그 기능을 통해 사용자의 질문과 챗봇 엔진의 출력 결과를 로그로 축적해 챗봇의 성능을 개선해나간다.
- 질문을 한시간, 질문내용, 의도종류, 정확도가 나옴

### 챗봇 api

- 챗봇 기능을 지원하는 메신저 플랫폼과 통신하기 위해서는 rest api방식으로 챗봇 서버를 구현해야함
- flask를 이용함
- rest api호출 시 챗봇 엔진 서버에 소켓 통신으로 접속해 질의에 대한 답변을 받아오는 api 서버를 chatbot_api/app.py로 생성


## 실행 화면

### 메인화면
---

![image](https://github.com/user-attachments/assets/42e44609-4e54-47a0-b867-48ebac993fc7)

### 회원가입
---

![image](https://github.com/user-attachments/assets/77b4c8cd-e9ac-4eee-9e3a-623151827475)

### 로그인
---

![image](https://github.com/user-attachments/assets/b893bb3f-493a-415c-9efd-8e0c0862fdb0)

### 챗봇 화면 
---

![image](https://github.com/user-attachments/assets/831b5a2c-67b6-41c4-9c1f-f308b3237f86)





## 궁금증

질문이나 피드백이 있는 경우 hun8529@gmail.com 으로 연락주세요.

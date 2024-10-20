#6번
#답변 검색 클래스

import torch
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer, util

class FindAnswer:
    def __init__(self, preprocess, df, embedding_data):
        # 챗봇 텍스트 전처리기
        self.p = preprocess

        # pre-trained SBERT
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

        # 질문 데이터프레임
        self.df = df

        # embedding_data
        self.embedding_data = embedding_data

    def search(self, query, intent):
        # 형태소 분석
        pos = self.p.pos(query)

        # 불용어 제거
        keywords = self.p.get_keywords(pos, without_tag=True)
        query_pre = ""
        for k in keywords:
            query_pre += str(k)

        # 전처리된 질문 인코딩 및 텐서화
        query_encode = self.model.encode(query_pre)
        query_tensor = torch.tensor(query_encode)

        # 코사인 유사도를 통해 질문 데이터 선택
        cos_sim = util.cos_sim(query_tensor, self.embedding_data)
        best_sim_idx = int(np.argmax(cos_sim))
        selected_qes = self.df['질문(Query)'][best_sim_idx]
        query_intent = self.df['의도(Intent)'][best_sim_idx]#추가(로그 기능)

        if self.df['의도(Intent)'][best_sim_idx] == intent:
            # 선택된 질문 문장 인코딩
            selected_qes_encode = self.model.encode(selected_qes)

            # 유사도 점수 측정
            score = dot(query_tensor, selected_qes_encode) / (norm(query_tensor) * norm(selected_qes_encode))

            # 답변
            answer = self.df['답변(Answer)'][best_sim_idx]
            imageUrl = self. df['답변 이미지'][best_sim_idx]

        else:
            #selected_qes = "nan"
            score = 0
            answer = self.df['답변(Answer)'][best_sim_idx]
            imageUrl = self. df['답변 이미지'][best_sim_idx]

        return selected_qes ,score, answer, imageUrl,query_intent
#전처리기를 통해 질문의 전처리가 이루어짐
#질문의 의도 파악 모델이 먼저 실행되기 때문에 선택된 질문의 의도와 모델이 계산한 의도가 일치하지 않는다면, 올바른 답변을 출력할 수 없게 설정함
#올바른 수행이 이루어졌는지 아닌지를 구분하기 위한 success 변수를 반환하도록 구현함
#이는 추후에 데이터 축적을 목적으로 로그를 남기기 위함.
 
 #순서
 #문장이 들어오면 
 #1. 전처리(형태소,품사 태거 / 불용어 제거)
 #2. 문장 임베딩처리(전처리된 문장 tensor화시킴(수치화))
 #3. 코사인 유사도를 이용해 질문답변 엑셀에서 '질문 데이터 선택'
 #4. 선택된 질문에서 의도(번호(0), 장소(1), 시간(2)) 선택
 #5. 최종적으로 선택된 질문 문장 인코딩하여 '유사도 점수 측정'
 #6. 유사도 점수가 가장 높은 답변 출력


 #로그 기능 추가로 인해 
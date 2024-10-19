# 4번
#임베딩 저장, 
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

import torch
from sentence_transformers import SentenceTransformer
#임베딩 클래스화
class create_embedding_data:
    def __init__(self, preprocess, df):
        #텍스트 전처리기
        self.p = preprocess

        #질문 데이터프레임
        self.df = df

        #pre-trained SBERT
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    
    def create_pt_file(self):
        #질문 목록 리스트
        target_df = list(self.df['질문(Query)'])

        #형태소 분석
        for i in range(len(target_df)):
            sentence = target_df[i]
            pos = self.p.pos(sentence)
            keywords = self.p.get_keywords(pos, without_tag=True)
            temp = ""
            for k in keywords:
                temp +=str(k)
            target_df[i]=temp
        
        self.df['질문 전처리'] = target_df
        self.df['embedding_vector'] = self.df['질문 전처리'].progress_map(lambda x: self.model.encode(x))

        embedding_data = torch.tensor(self.df['embedding_vector'].tolist())
        torch.save(embedding_data, './Train_tools/qna/embedding_data.pt')

#임베딩 저장 기능을 챗봇 엔진에서 사용하기 위해 클래스화 시켰다.

#이전 코드와 다른점은, 구현했던 텍스트 전처리기를 통해 질문 데이터를 pos태깅하고 불용어 제거를 진행한 후 임베딩을 진행했다.
#이는 유사도를 비교할 대상이 챗봇 사용자의 전처리된 입력이기 때문이다.
#따라서, 구축한 질문 데이터의 임베딩도 전처리 후 진행되도록 구현했다.


#################################################################################################################################

# # - 1
# train_file = './Train_tools/qna/train_data.xlsx'
# model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS') # 임베딩 모델 다운로드

# #- 2
# df = pd.read_excel(train_file)
# df['embedding_vector'] = df['질문(Query)'].progress_map(lambda x : model.encode(x))
# df.to_excel("train_data_embedding.xlsx", index = False)# 임베딩 처리된거 엑셀로 저장

# #- 3
# embedding_data = torch.tensor(df['embedding_vector'].tolist())
# torch.save(embedding_data, 'embedding_data.pt') # 모델 저장


# - 1
# 데이터 구축한 엑셀 파일과 사전 학습된 모델을 불러옴

# - 2
#엑셀 파일의 내용에서 '질문(Query)'열에 해당하는 내용만 필요하기 때문에 해당 부분 문장들에 대해 임베딩 진행
# 그 후 'embedding_vector'열을 만들어 엑셀 파일로 저장함

# - 3
#해당 임베딩 데이터를 torch.tonsor()를 통해 tensor화 시켜 embedding_data 파일명의 pt로 저장
# embedding_data.pt는 챗봇 엔진 구현에 사용될 예정

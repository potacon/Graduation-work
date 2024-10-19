# 3-1번
#의도분류 모듈 생성
#train_model.py에서 만든 의도 분류 모델로 생성 
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

#의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, preprocess):
        #의도 클래스별 레이블
        self.labels = {0:'번호', 1:'장소', 2:'시간', 3:'컴공관련', 4:'질문'}

        #의도 분류 모델 불러오기
        self.model = load_model(model_name)

        #preprocess 객체
        self.p = preprocess
    
    #의도 클래스 예측
    def predict_class(self, query):
        #형태소 분석
        pos = self.p.pos(query)

        #문장 내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기
        import os, sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from Config.GlobalParams import MAX_SEQ_LEN      

        #패딩 처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')
        
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0] 

#models/intent/train_model 
#의도분류 모델 테스트
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Utils.Preprocess import Preprocess
from Models.intent.IntentModel import IntentModel

p = Preprocess(word2index_idc='./chatbot_dict.bin', userdic='./Utils/user_dic.tsv')

intent = IntentModel(model_name='./intent_model.h5', preprocess= p )

query = "컴공 과사 번호 알려줘"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "전화번호 알려줘."
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "학교 도서관 번호는??"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "본관 건물 위치 어디야?"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "학교 운동장은 어디야?"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "기간 언제까지야?"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)

query = "컴퓨터공학부란?"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)
print("="*30)
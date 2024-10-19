# 3번
#의도 분류 모델 생성
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Utils.Preprocess import Preprocess
import pandas as pd
import tensorflow as tf
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate

#데이터 불러오기
data = pd.read_csv('./데이터/train_data.csv')
text = data['text'].tolist()
label = data['label'].tolist()

p = Preprocess(word2index_idc='./chatbot_dict.bin', userdic='./Utils/user_dic.tsv')

#단어 시퀀스 생성
#preprocess를 이용해 단어 시퀀스 생성 
#해당 단어에 매치되는 번호로 시퀀스를 생성함
sequences = []
for sentence in text:
    pos = p.pos(sentence)
    keywords = p.get_keywords(pos, without_tag=True)
    seq = p.get_wordidx_sequence(keywords)
    sequences.append(seq)

#단어 인덱스 시퀀스 벡터 생성 - 1
#단어 시퀀스 벡터 크기
from Config.GlobalParams import MAX_SEQ_LEN
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen = MAX_SEQ_LEN, padding = 'post')

#학습용, 검증용, 테스트용 데이터셋 생성 - 2
#7 : 2 : 1
ds = tf.data.Dataset.from_tensor_slices((padded_seqs, label))
ds = ds.shuffle(len(text))

train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_ds = ds.take(train_size).batch(20)
val_ds = ds.skip(train_size).take(val_size).batch(20)
test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

# 하이퍼 파라미터 설정
dropout_prob = 0.5
EMB_SIZE = 128
EPOCH = 3
VOCAB_SIZE = len(p.word_index) + 1 #전체 단어 개수

#CNN 모델 정의 - 3
#conv1d를 사용해 훈련을 진행 
#일단 3가지 시간, 장소, 번호에 관한 3가지 분류를 할 수 있도록 함
input_layer = Input(shape=(MAX_SEQ_LEN))
embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

conv1 = Conv1D(
    filters=128,
    kernel_size = 3,
    padding = 'valid',
    activation = tf.nn.relu)(dropout_emb)
pool1 = GlobalMaxPool1D()(conv1)

conv2 = Conv1D(
    filters=128,
    kernel_size=4,
    padding='valid',
    activation=tf.nn.relu)(dropout_emb)
pool2 = GlobalMaxPool1D()(conv2)

conv3 = Conv1D(
    filters=128,
    kernel_size=5,
    padding='valid',
    activation=tf.nn.relu)(dropout_emb)
pool3 = GlobalMaxPool1D()(conv3)

# 합치기
concat = concatenate([pool1,pool2,pool3])

hidden = Dense(128, activation = tf.nn.relu)(concat)
dropout_hidden = Dropout(rate = dropout_prob)(hidden)
logits = Dense(5, name='logits')(dropout_hidden) # logits은 나온 값들의 점수
predictions = Dense(5, activation = tf.nn.softmax)(logits)

#모델 생성 -
model = Model(inputs = input_layer, outputs = predictions)
model.compile(optimizer = 'adam', loss='sparse_categorical_crossentropy', metrics = ['accuracy'])

#모델 학습
model.fit(train_ds, validation_data = val_ds, epochs = EPOCH, verbose= 2)

#모델 평가(테스트 데이터셋 이용)
loss, accuracy = model.evaluate(test_ds, verbose=2)
print('accuracy: %f' %(accuracy * 100))
print('loss: %f' % (loss))

#모델 저장 
model.save('intent_model.h5')

# - 1
# 위에서 생성한 단어 시퀀스 벡터의 크기를 동일하게 맞추기 위해 패딩처리함

# - 2
# 패딩처리된 시퀀스  벡터 리스트와 label 리스트 전체를 데이터셋 객체로 만듦
# 데이터를 shuffle한 후 학습용, 검증용, 테스트용 7:2:1 비율로 분리함

# - 3
#케라스 함수형 모델 방식으로 구현함
#입력하는 문장을 의도 클래스로 분류하는 CNN 모델은 전처리된 입력 데이터를 단어 임베딩 처리 하는 영역,
#학섭공 필터와 연산을 통해 문장의 feature map을 추출하는 평탄화 하는 영역,
# 완전 연결 계층을 통해 감정별로 클래스를 분류하는 영역으로 구성됨

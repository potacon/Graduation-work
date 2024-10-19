# 1번
#전처리 모듈은 챗봇 엔진 내에서 자주 사용해서 클래스로 정의함
from konlpy.tag import Komoran
import pickle
import jpype

class Preprocess:
    def __init__(self, word2index_idc='', userdic=None):
        #단어 인덱스 사전 불러오기
        if(word2index_idc != ''):
            f = open(word2index_idc, "rb")
            self.word_index = pickle.load(f)
            f.close()
        else:
            self.word_index = None
        
        #형태소 분석기 초기화 - 1
        self.komoran = Komoran(userdic=userdic)
        
        #관계언, 기호, 어미, 접미사 품사 제외 - 2
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', ' EF', 'EC', 'ETN', 'ETM',
            'XSN','XSV', 'XSA'
        ]
    #형태소 분석기 pos 태거 - 3
    def pos(self, sentence):
        jpype.attachThreadToJVM()
        return self.komoran.pos(sentence)
    
    #불용어 제거 후 필요한 품사 정보만 가져오기 - 4
    def get_keywords(self, pos, without_tag = False):
        f = lambda x: x in self.exclusion_tags    
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list
    
    #단어 인덱스 시퀀스 변환 메서드 추가 - 5
    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []
        
        w2i = []
        for word in keywords:
            try:
                w2i.append(self.word_index[word])
            except KeyError:
                #해당 단어가 사전에 없는 경우 OOV 처리 
                w2i.append(self.word_index['OOV'])
        return w2i

# 1
# preprocess 클래스가 생성될 때 형태소 분석기 인스턴스 객체를 생성함
#한국어 형태소 분석기 komoran 사용
# userdic 인자에서는 사용자 정의 사전 파일의 경로를 입력할 수 있음

# 2
#해당 리스트에 정의된 품사들은 불용어로 정의되어 핵심 키워드에서 제외됨

# 3 
# komoran 형태소 분석기의 pos(형태소와 품사 태그 추출) 태거를 호출하는 메서드
#이 메서드는 preprocess 클래스 외부에서는 komoran을 호출할 일이 없게 하기 위함

# 4 
#불용어를 제거한 후 핵심 키워드 정보만 가져오는 함수
# self.exclustion_tags(불용어 리스트) 리스트에 해당하지 않는 품사 정보만 키워드로 저장

# 5
#입력한 문장은 단어 인덱스 사전을 이용해 단어 시퀀스 벡터로 변환하는 기능
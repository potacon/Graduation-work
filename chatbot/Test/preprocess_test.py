#전처리 모듈 테스트
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Utils.Preprocess import Preprocess
from konlpy.tag import Komoran

text = '컴공 과사 번호를 알려줘?...!'

#전처리 객체 생성
p = Preprocess(userdic='./Utils/user_dic.tsv')

#형태소 분석기 실행
pos = p.pos(text)
print(pos)
#품사 태그와 같이 키워드 출력
ret = p.get_keywords(pos, without_tag=False)
print(ret)
#품사 태그 없이 키워드 출력
ret = p.get_keywords(pos, without_tag=True)
print(ret)

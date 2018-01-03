import requests                  # 웹 페이지의 HTML을 가져오는 모듈
from bs4 import BeautifulSoup    # HTML을 파싱하는 모듈
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[ \n\t\{\}\[\]\/?.,;:|\)*~`!^\-_+@\#$%&\\\=\(\'\"\xa0]', '', text)
    #cleaned_text2 = re.sub('[등록일]','',cleaned_text)

    #cleaned_text = re.sub('[등록일,판매처 ]','',cleaned_text)
    return cleaned_text

#def cleanText(text):
#    parse = re.sub('[<>"=]', '', text)
#    return parse

base_url = 'http://www.imbak.co.kr/shop/goods/goods_list.php?category=013'
data = []
#http://www.imbak.co.kr/shop/goods/goods_list.php?category=019
for n in range(1):

    # 웹 페이지를 가져온 뒤 BeautifulSoup 객체로 만듦
    url = base_url.format(n+3)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('div', { 'class': 'cate_item' })    # <table class="table_develop3">을 찾음
    #div.summary_in > div.subject.subject_row2
    #span.price > span.n

                                # 데이터를 저장할 리스트 생성
    for ul in table.find_all('ul'):      # 모든 <tr> 태그를 찾아서 반복(각 지점의 데이터를 가져옴)
        #print(ul)
        lis = list(ul.find_all('li'))    # 모든 <td> 태그를 찾아서 리스트로 만듦

                                         # (각 날씨 값을 리스트로 만듦)
        for li in lis:                   # <td> 태그 리스트 반복(각 날씨 값을 가져옴)
            if li.find('div'):             # <td> 안에 <a> 태그가 있으면(지점인지 확인)


                try:
                    cate = clean_text(soup.find('div', {'class': 'cate_navi'}).text)
                    name = clean_text(li.find('p', {'class': 'goods_nm'}).text)
                    customer_price = clean_text(li.find('span', {'class': 'customer_price'}).text)
                    real_price = clean_text(li.find('span', {'class': 'real_price'}).text)
                except AttributeError as e:
                    print("None")
                    #data.append([name, "품절", "품절"])
                    data.append(["None", name, "품절", "품절"])
                else:
                    if customer_price and real_price == None:
                        print("None")
                        #data.append([name, "품절", "품절"])
                        data.append(["None", name, "none", "none"])
                    else:
                        #print(customer_price)
                        #data.append([name, customer_price, real_price])
                        data.append([cate, name, customer_price, real_price])


data

with open('Imbak_Mall.csv', 'w') as file:    # weather.csv 파일을 쓰기 모드로 열기
    file.write('Category, Product Name, Customer_Price(원), Real_Price(원)\n')                  # 컬럼 이름 추가
    for i in data:                                              # data를 반복하면서
        file.write('{0},{1},{2},{3}\n'.format(i[0], i[1], i[2], i[3]))    # 지점,온도,습도를 줄 단위로 저장

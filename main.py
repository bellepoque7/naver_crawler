'''
현재 작동 막힘
적용방법
크롤링할 스마트스토어 페이지 입력

'''
url = 'https://smartstore.naver.com/latin/products/10078570992'
'''
밀알왕순대: https://smartstore.naver.com/latin/products/10078570992
미미제면소만두:https://smartstore.naver.com/latin/products/4794297226
이사떡방: https://smartstore.naver.com/latin/products/5550127158
'''


from bs4 import BeautifulSoup
import re
import pandas as pd
import time
 
# selenium import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
1. 크롬 옵션설정과 객체 생성
'''

options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
# options.add_argument('headless') # headless 모드 설정 -> 해당 옵션 적용 시 PDF 다운 불가
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox') 

# 방법 1. 수동으로 로컬드라이브 잡아주기
# chrome_driver_path = r'chromedriver-win64/chromedriver.exe'
# print(chrome_driver_path)
# service = Service(executable_path=chrome_driver_path)

# 방법2: WebDriverManager를 사용하여 ChromeDriver 자동 설치 및 설정
service = Service(ChromeDriverManager().install())

# 웹드라이버 초기화
driver = webdriver.Chrome(service=service, options=options)

# wait seconds...

'''
2. 리뷰버튼 + 최신순 정렬 구현
'''
driver.implicitly_wait(3) # 3초안에 웹페이지 로딩되면 넘어가기
driver.get(url)
time.sleep(3)
#selenium으로 접속시 자동차단되는 현상 -> 새로고침 버튼 눌러서 해결
# try:
#     driver.find_element(By.CSS_SELECTOR, '#content > div > div > div > a.button.highlight').click()
# except:
#     pass
time.sleep(3)
#리뷰버튼 클릭
# driver.find_element(By.CSS_SELECTOR,'#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a').click()
# driver.find_element(By.CSS_SELECTOR,'#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a').click()
time.sleep(3)
#최신순버튼 클릭
# driver.find_element(By.CSS_SELECTOR,'#REVIEW > div > div._2LvIMaBiIO > div._2LAwVxx1Sd > div._1txuie7UTH > ul > li:nth-child(2) > a').click()
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[2]/div/div[3]/div[8]/div/div[3]/div[1]/div[1]/ul/li[2]/a"))
)
element.click()

time.sleep(3)



'''
3. 데이터를 저장하기 위한 지료 초기화
'''
write_lst = []
rate_lst = []
item_lst =[]
tag_lst = []
content_lst =[]
start = time.time()


# 현재 페이지
page_num = 1
# 날짜 
date_cut = (datetime.now() - timedelta(days = 365)).strftime('%Y%m%d')
while True :
    if page_num % 10 == 0:
        print(f'start : {page_num} page 수집 중')
    # 1. 셀레니움으로 html가져오기
    html_source = driver.page_source
    # 2. bs4로 html 파싱
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)
    # 3. 리뷰 정보 가져오기
    reviews = soup.findAll('li', {'class': 'BnwL_cs1av'})
    
    # 4. 한페이지 내에서 수집 가능한 리뷰 리스트에 저장
    for review in range(len(reviews)):
        # 4-1. 평점 저장
        rate_raw = reviews[review].findAll('em' ,{'class' : '_15NU42F3kT'})[0].get_text()

        # 4-2. 태그 이름 저장
        #태그가 상품별로 몇개일지 알수없어서 일단 한컬럼에 저장
        tag_raw = ''
        tag_list = reviews[review].findAll('div' ,{'class' : '_1QLwBCINAr'})
        for tag in tag_list:
            tag_raw += tag.get_text()
            tag_raw += ','
        tag_raw.rstrip(',')

        # 4-3.리뷰작성일자 수집
        write_raw = reviews[review].findAll('span' ,{'class' : '_2L3vDiadT9'})[0].get_text()
        write_dt = datetime.strptime(write_raw, '%y.%m.%d.').strftime('%Y%m%d')

        # 4-4.상품명 수집
        # 4-4-(1) 상품명이 포함된 css 선택자 입력 
        item_nm_info_raw = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].get_text()

        # 4-4-(2) re.sub() 를 활용해 dl class="XbGQRlzveO"부분부터 추출한 문장을 공백으로 대체
        sentence = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].find('dl', {'class' : 'XbGQRlzveO'})
        if sentence != None:
            item_nm_info_for_del = sentence.get_text()
        else:
            item_nm_info_for_del = ''

        # 4-4-(3) re.sub(pattern, replacement, string) : string에서 pattern에 해당하는 부분을 replacement로 모두 대체
        item_nm_info= re.sub(item_nm_info_for_del, '', item_nm_info_raw)

        # 4-4-(4) find() : 문자열 순서 (인덱스) 반환 : find()를 활용해 '제품 선택 : '이 나오는 인덱스 반환
        str_start_idx = re.sub(item_nm_info_for_del, '', item_nm_info_raw).find('제품 선택: ')

        # 4-4-(5) 제품명만 추출. strip(): 공백 제거 
        item_nm = item_nm_info[str_start_idx + 6:].strip()


        # 5. 리뷰내용 수집
        review_content_raw = reviews[review].findAll('div', {'class' : '_1kMfD5ErZ6'})[0].find('span', {'class' : '_2L3vDiadT9'}).get_text()
        review_content = re.sub(' +', ' ',re.sub('\n',' ',review_content_raw ))

        # 6. 수집데이터 저장
        write_lst.append(write_dt)
        tag_lst.append(tag_raw)
        rate_lst.append(rate_raw)
        item_lst.append(item_nm)
        content_lst.append(review_content)
 
    #다음 버튼 있으면 클릭
    try:
        driver.find_element(By.CSS_SELECTOR,f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a.fAUKm1ewwo._2Ar8-aEUTq._nlog_click').click()
    except:
        break
    page_num += 1
print('done')    

'''
4. 데이터프레임 저장
'''

result_df = pd.DataFrame({
              'ITEM_NM' : item_lst,
              'RATE' : rate_lst,
              'CONTENT' : content_lst,
              'TAG' : tag_lst,
              'WRITE_DT' : write_lst })
print(result_df.head())
timenow = datetime.now().strftime("%Y%m%d_%H%M")
end = time.time()
long = (end - start) // 60 
print(f'총 {long} 분 소요 되었습니다.')
result_df.to_csv(f'./result_{timenow}.csv', encoding='utf-8-sig')

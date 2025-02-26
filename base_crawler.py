# 구글 검색을 위한 크롤러 기본 코드
# Window 11

# selenium import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 

# 옵션 설정
# 하기 옵션을 넣지않으면 봇으로 감지해서 reCAPCHA와 같은 단계가 생기기 때문에, 옵션에서 사람인것 처럼 설정

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
# 하기 옵션을 넣지않으면 봇으로 감지해서 reCAPCHA와 같은 단계가 생기기 때문에, 옵션에서 사람인것 처럼 설정
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")


service = Service(ChromeDriverManager().install())

# 웹드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Google 검색 페이지 열기
driver.get("https://www.google.com")

try:
    # 구글 홈페이지 열기
    driver.get("https://www.google.com")

    # 검색창 찾기
    search_box = driver.find_element(By.NAME, "q")

    # 검색어 입력 및 검색 실행
    search_query = "Python Selenium tutorial"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)  # Enter 키 누르기

    # 결과 로딩 대기
    time.sleep(2)

    # 첫 번째 검색 결과 가져오기
    first_result = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[12]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/span/a/h3")
    print("첫 번째 검색 결과 제목:", first_result.text)

    # 첫 번째 검색 결과 클릭
    first_result.click()

    # 추가 작업을 위해 몇 초 대기
    time.sleep(5)

finally:
    # 브라우저 닫기
    driver.quit()

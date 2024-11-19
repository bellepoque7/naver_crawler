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
    first_result = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[12]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/span/a/h3")
    print("첫 번째 검색 결과 제목:", first_result.text)

    # 첫 번째 검색 결과 클릭
    first_result.click()

    # 추가 작업을 위해 몇 초 대기
    time.sleep(5)

finally:
    # 브라우저 닫기
    driver.quit()

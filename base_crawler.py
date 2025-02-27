# 구글 검색을 위한 크롤러 기본 코드
# Window 11

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 
import pandas as pd

# 옵션 설정
# 하기 옵션을 넣지않으면 봇으로 감지해서 reCAPCHA와 같은 단계가 생기기 때문에, 옵션에서 사람인것 처럼 설정

'''
1. 크롬 옵션설정과 객체 생성
'''

options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
# options.add_argument('headless') # headless 모드 설정 -> 해당 옵션 적용 시 PDF 다운 불가
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox') 
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-webgl")

# 하기 옵션을 넣지않으면 봇으로 감지해서 reCAPCHA와 같은 단계가 생기기 때문에, 옵션에서 사람인것 처럼 설정
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



# 웹드라이버 초기화

def get_click():
    service = Service(ChromeDriverManager().install())
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
        first_result = driver.find_element(By.CSS_SELECTOR, "#rso > div:nth-child(1) > div > div > div > div.kb0PBd.A9Y9g.jGGQ5e > div > div > span > a > h3")
        print("첫 번째 검색 결과 제목:", first_result.text)

        # 첫 번째 검색 결과 클릭
        first_result.click()


    finally:
        # 브라우저 닫기
        # driver.quit()
        pass


def get_titles():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com/search?q=selenium+python")


        # 검색 결과에서 제목(h3)과 링크(a) 가져오기
        results = driver.find_elements(By.XPATH, "//h3/ancestor::a")


        titles = []
        links = []
        for result in results:
            title = result.text  # 제목
            link = result.get_attribute("href")  # 링크
            # print(f"제목: {title}\n링크: {link}\n")
            titles.append(title)
            links.append(link)

        pd.DataFrame({'제목':titles, '링크': links}).to_csv('./result.csv', encoding= 'utf-8-sig')

    finally:
        # 브라우저 닫기
        driver.quit()

if __name__ == "__main__":
    print('''
          선택지를 고르세요.
          1. 첫번째 제목 클릭하기
          2. 구글검색 후 제목 10개 수집하기 to pandas
          ''')
    choice = input()
    if choice == '1':
        get_click()
    elif choice == '2':
        get_titles()
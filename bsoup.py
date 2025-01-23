from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# 웹 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 크롤링할 핀터레스트 URL 설정 (네일 검색 결과 페이지로 일단)
URL = 'https://kr.pinterest.com/search/pins/?q=%EB%84%A4%EC%9D%BC&rs=typed'

# 페이지 열기
driver.get(URL)

# 블록방지 및 매너, 시간 간격 주기
time.sleep(3)  
from bs4 import BeautifulSoup

# 페이지 소스 가져오기
html = driver.page_source

# BeautifulSoup로 파싱
soup = BeautifulSoup(html, 'html.parser')

# 파싱된 HTML 구조 확인
#print(soup.prettify()[:2000])  # 처음 2000자만 출력하여 구조 확인
# 이미지 태그 모두 찾기
image_tags = soup.find_all('img')

#print(f"발견된 이미지 태그 수: {len(image_tags)}")

# 일부 이미지 태그 출력하여 구조 확인
#for img in image_tags[:5]:
#     print(img)

image_urls = []

for img in image_tags:
#     # src 또는 data-src 속성에서 이미지 URL 가져오기
     img_url = img.get('src') or img.get('data-src')
     if img_url and img_url.startswith('http'):
         image_urls.append(img_url)

# print(f"추출된 이미지 URL 수: {len(image_urls)}")
# print("예시 이미지 URL:", image_urls[:5])

import os
import requests

# 이미지 저장 디렉토리 설정
save_dir = 'pinterest_nail_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 이미지 다운로드
headers = {
    'User-Agent': 'Mozilla/5.0'
    }

for idx, img_url in enumerate(image_urls):
    try:
        # 이미지 요청
        img_data = requests.get(img_url, headers=headers).content
        # 이미지 파일 경로 설정
        img_file = os.path.join(save_dir, f'image_{idx+1}.jpg')
        # 이미지 저장
        with open(img_file, 'wb') as handler:
            handler.write(img_data)
        print(f"이미지 {idx+1} 저장 완료: {img_file}")
    except Exception as e:
        print(f"이미지 {idx+1} 저장 실패: {e}")


        # 스크롤하여 추가 이미지 로드
for i in range(5):  # 스크롤 횟수 설정
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # 스크롤 후 로딩 대기

# 페이지 소스 다시 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 이미지 태그 다시 찾기
image_tags = soup.find_all('img')

# 기존 이미지 URL 리스트에 추가하지 않고 새로운 URL만 추가
for img in image_tags:
    img_url = img.get('src') or img.get('data-src')
    if img_url and img_url.startswith('http') and img_url not in image_urls:
        image_urls.append(img_url)

print(f"추가 추출된 이미지 URL 수: {len(image_urls)}")
print("예시 추가 이미지 URL:", image_urls[-5:])

# 브라우저 종료
driver.quit()

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ---------------------------------------
# 1) 여러 개의 검색어(폴더명) 설정
# ---------------------------------------
search_keywords = [
    "겨울_네일",
    "trend_2025_nail",
    "이달의네일",
    "짧은손톱네일",
    "귀여운네일",
    "프렌치네일",
    "자석네일",
    "세련된네일",
    "글리터네일"
]

# 핀터레스트 기본 URL (검색어 붙여서 사용)
BASE_URL = "https://kr.pinterest.com/search/pins/?q="

# ---------------------------------------
# 2) srcset 중 가장 큰 이미지 URL 추출 함수
# ---------------------------------------
def get_largest_image_from_srcset(srcset_value: str) -> str:
    """
    srcset 속성: "이미지URL_1 w1, 이미지URL_2 w2, ..."
    → 쉼표로 구분된 마지막 항목(가장 큰 해상도)을 골라서 반환
    """
    bigpic = [url.strip() for url in srcset_value.split(',')]
    # 마지막 항목(가장 큰 w 값)
    largest_bigpic = bigpic[-1]
    # "https://...jpg 564w" → ["https://...jpg", "564w"]
    largest_url = largest_bigpic.split()[0]
    return largest_url


# ---------------------------------------
# 3) 특정 검색어로 핀터레스트 이미지를 크롤링 & 다운로드하는 함수
# ---------------------------------------
def crawl_pinterest_images(keyword: str, scroll_times: int = 5, base_folder: str = "pinterest_images"):
    """
    keyword: 핀터레스트에서 검색할 키워드 겸, 폴더명
    scroll_times: 스크롤 횟수 (더 늘리면 더 많은 이미지)
    base_folder: 전체 이미지 저장 루트 폴더
    """

    # 1) 폴더 경로 준비
    save_dir = os.path.join(base_folder, keyword)
    os.makedirs(save_dir, exist_ok=True)

    # 2) Pinterest 검색 페이지 열기
    search_url = f"{BASE_URL}{keyword}&rs=typed"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(search_url)

    time.sleep(3)  # 페이지 로딩 대기

    # 3) 초기 페이지 소스 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    image_tags = soup.find_all("img")

    image_urls = []

    # 4) 첫 페이지에서 이미지 URL 추출
    for img in image_tags:
        srcset = img.get("srcset")
        if srcset:
            # srcset이 있으면 가장 큰 해상도 URL
            largest_url = get_largest_image_from_srcset(srcset)
            if largest_url.startswith("http"):
                image_urls.append(largest_url)
        else:
            # fallback: src / data-src
            img_url = img.get("src") or img.get("data-src")
            if img_url and img_url.startswith("http"):
                image_urls.append(img_url)

    # 5) 추가 스크롤로 더 많은 이미지 로딩
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤 후 로딩 대기

    # 스크롤 후 다시 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    image_tags = soup.find_all("img")

    # 새로 나온 이미지 URL들 추가
    for img in image_tags:
        srcset = img.get("srcset")
        if srcset:
            largest_url = get_largest_image_from_srcset(srcset)
            # 중복 체크
            if largest_url.startswith("http") and (largest_url not in image_urls):
                image_urls.append(largest_url)
        else:
            img_url = img.get("src") or img.get("data-src")
            if img_url and img_url.startswith("http") and (img_url not in image_urls):
                image_urls.append(img_url)

    print(f"[{keyword}] 총 수집된 이미지 URL: {len(image_urls)}")

    # 6) 이미지 다운로드
    headers = {"User-Agent": "Mozilla/5.0"}

    for idx, url in enumerate(image_urls, start=1):
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                file_path = os.path.join(save_dir, f"image_{idx}.jpg")
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                print(f"    {idx}/{len(image_urls)} 저장 완료: {file_path}")
            else:
                print(f"    [오류] {idx}번째 이미지, 상태코드: {resp.status_code}")
        except Exception as e:
            print(f"    [오류] {idx}번째 이미지 다운로드 실패: {e}")

    # 7) 드라이버 종료
    driver.quit()


# ---------------------------------------
# 4) 메인 실행부: 모든 검색어 한 번에 진행
# ---------------------------------------
if __name__ == "__main__":
    for keyword in search_keywords:
        print(f"=== '{keyword}' 검색 시작 ===")
        crawl_pinterest_images(keyword=keyword, scroll_times=5, base_folder="pinterest_images")
        print()

import os  # 파일 및 디렉토리 관리를 위한 모듈
import time  # 시간 지연을 위한 모듈
import requests  # HTTP 요청을 보내기 위한 모듈
from selenium import webdriver  # 웹 브라우저 자동화를 위한 모듈
from selenium.webdriver.chrome.service import Service  # ChromeDriver 서비스 설정
from selenium.webdriver.common.by import By  # 웹 요소를 찾기 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriver 자동 설치를 위한 모듈
from urllib.parse import quote  # URL 인코딩을 위한 모듈
import json  # JSON 데이터 처리
import re  # 정규 표현식을 위한 모듈

# ---------------------------------------
# 1) 여러 개의 검색어(폴더명) 설정
# ---------------------------------------
search_keywords = [
    "이달아",
    "이달의 아트",
    "겨울 네일",
    "짧은 손톱 네일",
    "귀여운 네일",
    "자석 네일",
    "세련된 네일",
    "글리터 네일",
    "화려한 네일",
    "ネール・アート"
]

# Pinterest 기본 URL (검색어를 붙여서 사용)
BASE_URL = "https://kr.pinterest.com/search/pins/?q="

# ---------------------------------------
# 2) 파일 이름 정제 함수
# ---------------------------------------
def sanitize_filename(name):
    """
    파일 이름에 사용할 수 없는 문자를 제거하거나 대체합니다.
    :param name: 원본 파일 이름
    :return: 정제된 파일 이름
    """
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# ---------------------------------------
# 3) 이미지 다운로드 함수
# ---------------------------------------
def download_image(url, save_path):
    """
    주어진 URL에서 이미지를 다운로드하고 지정된 경로에 저장합니다.
    :param url: 이미지 URL
    :param save_path: 이미지를 저장할 경로
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code == 200:  # 요청이 성공한 경우
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download: {url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# ---------------------------------------
# 4) 이미지 URL 크기 변경 함수
# ---------------------------------------
def replace_image_size(url, original_size="60x60", new_size="736x"): #(!!!여기서 url None 발생//Nonetype 객체 반복 불가)
    
 #---------------수정-----------------
 # url이 None 이거나 빈 문자열이면 그대로 반환 (혹은 None 반환) 
    if not url:
        return url
 # --------------수정-----------------   
    """
    이미지 URL의 크기를 변경하는 함수.
    :param url: 원본 이미지 URL
    :param original_size: 변경 전 크기 (기본값: "60x60")
    :param new_size: 변경 후 크기 (기본값: "736x")
    :return: 수정된 이미지 URL
    """
    if original_size in url:  # 원본 크기가 URL에 포함된 경우 
        return url.replace(original_size, new_size)  # 크기 변경
    return url  # 크기 변경이 불가능한 경우 원본 URL 반환

# ---------------------------------------
# 5) Pinterest API 요청 함수
# ---------------------------------------
def fetch_pinterest_api(keyword):
    """
    Pinterest API를 통해 검색 결과를 가져옵니다.
    :param keyword: 검색어
    :return: API 응답 데이터 (JSON 형식) 또는 None
    """
    api_url = (
        f"https://kr.pinterest.com/resource/BaseSearchResource/get/"
        f"?source_url=%2Fsearch%2Fpins%2F%3Fq%3D{quote(keyword)}"
        f"&data=%7B%22options%22%3A%7B%22query%22%3A%22{quote(keyword)}%22%7D%7D"
    )
    
    try:
        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code == 200:
            return response.json()  # JSON 데이터 반환
        else:
            print(f"Failed to fetch API for '{keyword}'. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching API for '{keyword}': {e}")
        return None

# ---------------------------------------
# 6) 연관 검색어 및 이미지 크롤링 함수
# ---------------------------------------
def crawl_related_data(data, base_folder, keyword):
    """
    연관 검색어 및 이미지를 크롤링합니다.
    :param data: API 응답 데이터 (JSON 형식)
    :param base_folder: 이미지를 저장할 기본 폴더
    :param keyword: 검색어
    """
    if not data:
        return

    # 연관 검색어 폴더 생성
    related_folder = os.path.join(base_folder, keyword, "related")
    os.makedirs(related_folder, exist_ok=True)

    # 연관 검색어 데이터 추출
    ranked_guides = data.get("resource_response", {}).get("data", {}).get("rankedGuides", [])
    print(f"[DEBUG] 연관 검색어 개수: {len(ranked_guides)}")

    for i, guide in enumerate(ranked_guides):

#------------수정 (guide 자체가 None 일수도 있음 방어코드 추가)------------
        if not guide:
            continue
#------------수정 (guide 자체가 None 일수도 있음 방어코드 추가)------------
        term = guide.get("term", "NoTerm")  # 연관 검색어
                
        #수정image_url = guide.get("image_medium_url", "NoImage")  # 연관 검색어 이미지
        #'image_medium_url'이 존재하되 값이 None이면 "NoImage"로 대체

        image_url = guide.get("image_medium_url") or "NoImage" 

        # 파일 이름 정제
        term_clean = sanitize_filename(term)

        # 이미지 URL 크기 변경
        large_image_url = replace_image_size(image_url, original_size="60x60", new_size="736x")

        # 이미지 다운로드
        if image_url != "NoImage":
            save_path = os.path.join(related_folder, f"{term_clean}_{i}.jpg")
            download_image(large_image_url, save_path)

# ---------------------------------------
# 7) Pinterest 이미지 크롤링 함수
# ---------------------------------------
def crawl_pinterest_images(keyword, scroll_times, base_folder):
    """
    Pinterest에서 특정 검색어로 이미지를 크롤링하고 다운로드합니다.
    :param keyword: 검색어
    :param scroll_times: 스크롤 횟수 (더 많은 이미지를 로드하기 위해)
    :param base_folder: 이미지를 저장할 기본 폴더
    """
    # 검색어별 폴더 생성
    save_folder = os.path.join(base_folder, keyword)
    os.makedirs(save_folder, exist_ok=True)

    # 웹 드라이버 설정 (ChromeDriver 자동 설치)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 실행
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # 추가적인 안정성 옵션
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=options)

    try:
        # Pinterest 검색 페이지로 이동
        search_url = BASE_URL + quote(keyword)
        driver.get(search_url)
        time.sleep(3)  # 페이지 로딩 대기

        # 스크롤을 통해 더 많은 이미지 로드
        for _ in range(scroll_times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 스크롤 후 로딩 대기

        # 이미지 URL 수집
        images = driver.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]

        # 중복 체크를 위한 세트
        downloaded_urls = set()

        # 이미지 다운로드
        for i, url in enumerate(image_urls):
            if url and url not in downloaded_urls:
                downloaded_urls.add(url)
                # 이미지 URL 크기 변경 (작은 크기 → 큰 크기)
                large_image_url = replace_image_size(url, original_size="60x60", new_size="736x")
                save_path = os.path.join(save_folder, f"{keyword}_{i}.jpg")
                download_image(large_image_url, save_path)

        # 연관 검색어 및 이미지 크롤링
        api_data = fetch_pinterest_api(keyword)
        crawl_related_data(api_data, base_folder, keyword)

    except Exception as e:
        print(f"Error during crawling '{keyword}': {e}")
    finally:
        driver.quit()

# ---------------------------------------
# 8) 메인 실행부
# ---------------------------------------
if __name__ == "__main__":
    """
    모든 검색어에 대해 Pinterest 이미지 크롤링을 실행합니다.
    """
    base_folder = "pinterest_images1"
    os.makedirs(base_folder, exist_ok=True)

    for keyword in search_keywords:
        print(f"=== '{keyword}' 검색 시작 ===")
        crawl_pinterest_images(keyword=keyword, scroll_times=10, base_folder=base_folder) #scroll 5 → 10으로 변경
        print()
    print("모든 작업이 완료되었습니다.")
# 네일아트 디자인 크롤링 도구

## 소개
매달 네일아트를 위해 다양한 디자인을 검색하는 과정에서 많은 시간을 소모하게 되나요? 이 프로젝트는 Pinterest에서 네일아트 이미지를 자동으로 크롤링하고, 
키워드별로 정리하여 효율적으로 디자인을 선택할 수 있도록 도와줍니다. Streamlit을 활용한 사용자 친화적인 인터페이스를 통해 최종 디자인 결정을 손쉽게 할 수 있습니다.

## 목차
- [프로젝트 선택 이유](#프로젝트-선택-이유)
- [문제 인식](#문제-인식)
- [해결 방안](#해결-방안)
  - [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [폴더 구조](#폴더-구조)
- [설치 및 실행](#설치-및-실행)
  - [사전 요구사항](#사전-요구사항)
  - [설치](#설치)
  - [크롤링 실행](#크롤링-실행)
  - [Streamlit 앱 실행](#streamlit-앱-실행)
- [사용 방법](#사용-방법)

## 프로젝트 선택 이유
- **개인적인 필요성**: 매달 네일아트를 위해 다양한 디자인을 검색하는 과정에서 시간 소모와 비효율성 경험
- **시장 수요**: 네일아트 디자인의 다양성과 사용자들의 빠르고 효율적인 디자인 선택에 대한 요구 증가
- **기술적 도전**: 웹 크롤링과 데이터 정리를 자동화하여 문제를 해결하는 기술적 가능성 탐구

## 문제 인식
매달 네일아트를 위해 다양한 디자인을 찾기 위해 여러 번의 검색어 입력과 페이지 방문을 반복하면서 많은 시간을 소비하게 됩니다. 
이러한 비효율적인 검색 과정을 개선하고, 원하는 디자인을 빠르게 찾기 위해 이미지들을 체계적으로 정리할 필요가 있습니다.

## 해결 방안
Pinterest에서 원하는 키워드로 이미지를 크롤링하여 저장하고, 이를 키워드별 폴더로 분류하여 관리합니다. 
수집된 이미지를 바탕으로 아이디어를 종합하고 최종 디자인을 선택하는 과정을 Streamlit 앱으로 구현하여 사용자에게 편리한 인터페이스를 제공합니다.

### 주요 기능
1. **Pinterest 이미지 크롤링**
   - 키워드별 이미지 자동 다운로드
   - 연관 검색어 이미지 추가 수집

2. **폴더 구조화**

pinterest_images/      
    ├── 이달아/       
    ├── 이달의 아트/     
    ├── 겨울 네일/     
    ├── 짧은 손톱네일/    
    ├── 귀여운 네일/     
    ├── 자석 네일/     
    ├── 세련된 네일/    
    ├── 글리터 네일/     
    ├── 화려한 네일/      
    └── ネール・アート/     
    
    **각 폴더별로 related 폴더도 생성**
    
   - 키워드별 폴더 생성 및 이미지 정리
   - 새로운 키워드 추가 시 자동 폴더 생성
     

3. **Streamlit 앱 구현**
   - 수집된 이미지를 시각적으로 정리
   - 간편한 UI를 통해 최종 디자인 선택

## 기술 스택
- **프로그래밍 언어**: Python
- **웹 크롤링**: Selenium, Requests
- **웹 애플리케이션**: Streamlit
- **기타 라이브러리**: BeautifulSoup, webdriver_manager등

## 폴더 구조
프로젝트는 다음과 같은 폴더 구조로 이미지를 정리합니다:

- **검색어 목록**에 따른 폴더 생성
- 새로운 키워드 추가 시 폴더 자동 생성
- `related/` 폴더에는 연관 검색어로 수집된 이미지가 저장됩니다.

## 설치 및 실행

### 사전 요구사항
- Python 3.8 이상
- pip 패키지 관리자

### 설치
1. 저장소를 클론합니다.

2. 필요한 패키지를 설치합니다.

### 크롤링 실행
크롤링 스크립트를 실행하여 Pinterest에서 이미지를 다운로드하고 폴더에 저장합니다.

nail_art.py

Streamlit 앱 실행
Streamlit 앱을 실행하여 수집된 이미지를 시각적으로 확인하고 최종 디자인을 선택합니다.

```bash
streamlit run nail_app.py
```

사용 방법
크롤링 설정: nail_art.py 파일 내 search_keywords 리스트에 원하는 검색어를 추가하거나 수정합니다.

크롤링 실행: 위의 크롤링 실행 단계를 따라 스크립트를 실행하여 이미지를 다운로드하고 폴더에 저장합니다. (폴더명 변경가능합니다.)

코드에서 
- - - - - - - - -- ---- ----- --------------------
    8) 메인 실행부
 - - - - - - - - ----- ----- --- -----------------
  를 찾아 그 밑에 작성 된 쌍따옴표 안의 문자열을 변경하세요. (필요하시다면)
   **base_folder = "pinterest_images1"** (← 여기를 찾으세요)

   
앱 사용: Streamlit 앱을 실행한 후 웹 브라우저에서 열리는 인터페이스를 통해 저장된 이미지를 확인하고 최종 디자인을 선택합니다.


import streamlit as st
import os
from PIL import Image

# -----------------------------
# 0) 기본 설정
# -----------------------------
BASE_FOLDER = "pinterest_images1"  # 크롤링 결과가 들어있는 폴더

st.title("Pinterest Nail ideas")

# -----------------------------
# 1) 이미지 로딩 함수 (먼저 정의 )
# -----------------------------

#----------------cache추가 -----------------------------------
@st.cache_data
def load_image(image_path):
    """
    이미지를 로드하고, 캐싱하여 중복 로드를 방지합니다.
    :param image_path: 이미지 파일 경로
    :return: PIL.Image 객체
    """
    return Image.open(image_path)

# -----------------------------
# 2) 상위 폴더(검색어 목록) 불러오기
# -----------------------------


@st.cache_data
def get_search_folder(base_folder):
    if not os.path.exists(base_folder):
        return None
    return[
        f for f in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, f))
    ]

search_folders = get_search_folder(BASE_FOLDER)

if search_folders is None:
    st.error(f"'{BASE_FOLDER}' 폴더가 존재하지 않습니다. 먼저 크롤링을 진행해주세요")
    st.stop()

# if not os.path.exists(BASE_FOLDER):
#     st.error(f"'{BASE_FOLDER}' 폴더가 존재하지 않습니다. 먼저 크롤링을 진행해주세요.")
#     st.stop()

# 검색어 폴더 리스트 (디렉토리만 추출)
# search_folders = [
#     f for f in os.listdir(BASE_FOLDER) 
#     if os.path.isdir(os.path.join(BASE_FOLDER, f))
# ]
#----------------cache추가 --------------------------------------


if not search_folders:
    st.warning("아직 크롤링된 폴더가 없습니다.")
    st.stop()


# 사용자에게 선택받을 검색어(폴더)
selected_search_folder = st.selectbox("검색어(폴더)를 선택하세요:", search_folders)

# -----------------------------
# 3) 'related' 폴더 체크
# -----------------------------


#---------------추가---------------------------------------------
def get_related_folder_path(base_folder, search_folder):
    return os.path.join(base_folder, search_folder,"related")
#---------------------------------------------------------------------

#selected_search_path = os.path.join(BASE_FOLDER, selected_search_folder)

related_folder_path = get_related_folder_path(BASE_FOLDER, selected_search_folder) #수정

has_related = os.path.exists(related_folder_path) and os.path.isdir(related_folder_path)

# 기본 폴더 vs related 폴더 선택
folder_options = ["(기본 폴더)"]
if has_related:
    folder_options.append("related")

selected_subfolder = st.radio("상세 폴더를 선택하세요:", folder_options)

# 실제 보여줄 폴더 경로
if selected_subfolder == "related":
    target_folder_path = related_folder_path
else:
    target_folder_path = os.path.join(BASE_FOLDER, selected_search_folder) #수정

# -----------------------------
# 4) 선택된 폴더 내의 이미지 표시
# -----------------------------

st.header(f"폴더: {selected_search_folder} / {selected_subfolder}")

#-------캐싱 추가 ---------------------------------------------
@st.cache_data
def get_image_files(folder_path):
        
        # 유효한 이미지 확장자
    valid_extensions=(".jpg", ".jpeg", ".png", ".gif")  
    return[
        f for f in os.listdir(folder_path)
        if f.lower().endswith(valid_extensions)
    ]

# 유효한 이미지 확장자
#    valid_extensions=(".jpg", ".jpeg", ".png", ".gif") 
# image_files = [
#     f for f in os.listdir(target_folder_path)
#     if f.lower().endswith(valid_extensions)
# ]
#-----------------------------------------------------------------------
image_files = get_image_files(target_folder_path) 

if not image_files:
    st.write("이미지가 없습니다.")
else:
    st.write(f"총 {len(image_files)}개의 이미지가 있습니다.")
    
    # 한 줄에 3개씩 컬럼으로 나눠서 보여주기
    cols = st.columns(3)
    
    for idx, img_name in enumerate(image_files):
        img_path = os.path.join(target_folder_path, img_name)
        image = load_image(img_path)
        with cols[idx % 3]:
            # use_column_width -> use_container_width 로 변경(최신버전 때문에)
            st.image(image, caption=img_name, use_container_width=True)

# # -----------------------------
# # 5) 이미지 로딩 함수(먼저 정의해야해서 1번으로 이동)
# # -----------------------------

# @st.cache_data
# def load_image(image_path):
#     try:
#         return Image.open(image_path)
#     except Exception as e:
#         st.error(f"이미지 로딩 오류:{e}")
#         return None


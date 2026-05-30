import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

# 1. 페이지 설정 및 애니메이션 디자인 (CSS)
st.set_page_config(page_title="Project Nightfall", layout="wide", initial_sidebar_state="collapsed")

# 별이 내리는 효과와 검은색 테마, 버튼 중앙 정렬을 위한 CSS 강제 주입
st.markdown("""
    <style>
    /* 전체 배경을 딥블랙으로 설정 */
    .stApp {
        background-color: #020617;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* 별이 내리는 애니메이션 효과 */
    @keyframes falling_stars {
        0% { transform: translateY(-10vh) translateX(0px) rotate(45deg); opacity: 1; }
        100% { transform: translateY(110vh) translateX(200px) rotate(45deg); opacity: 0; }
    }
    .star {
        position: fixed;
        width: 2px;
        height: 2px;
        background: white;
        border-radius: 50%;
        z-index: 0;
        pointer-events: none;
    }
    .s1 { left: 15%; animation: falling_stars 6s linear infinite; }
    .s2 { left: 40%; animation: falling_stars 9s linear infinite; animation-delay: 1s; }
    .s3 { left: 70%; animation: falling_stars 5s linear infinite; animation-delay: 2s; }
    .s4 { left: 90%; animation: falling_stars 10s linear infinite; animation-delay: 0.5s; }

    /* 망원경 렌즈 효과 (Telescope Mask) */
    .telescope-lens {
        width: 380px;
        height: 380px;
        border-radius: 50%;
        border: 12px solid #1e293b;
        box-shadow: 0 0 60px rgba(251, 191, 36, 0.3);
        margin: 20px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        background: radial-gradient(circle, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 85%);
    }

    /* 🔥 [핵심 추가] 스트림릿 고유 엘리먼트까지 통제하여 무조건 가로 중앙 정렬 */
    .stButton, div.stButton, .element-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* 고급 컨설팅 스타일 버튼 커스텀 */
    div.stButton > button {
        background-color: transparent !important;
        color: #fbbf24 !important;
        border: 2px solid #fbbf24 !important;
        padding: 12px 60px !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        transition: 0.4s !important;
        margin: 20px auto !important; /* 위아래 여백을 주고 좌우를 auto로 두어 정중앙 고정 */
    }
    
    div.stButton > button:hover {
        background-color: #fbbf24 !important;
        color: #020617 !important;
        box-shadow: 0 0 25px #fbbf24 !important;
    }

    /* 텍스트 스타일링 */
    .main-title { font-size: 75px; font-weight: 800; text-align: center; margin-top: 100px; color: #f8fafc; }
    .gold { color: #fbbf24; }
    </style>
    
    <div class="star s1"></div><div class="star s2"></div>
    <div class="star s3"></div><div class="star s4"></div>
    """, unsafe_allow_html=True)

# 2. 세션 상태 관리 (화면 전환 제어)
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

# 3. 데이터 로드
@st.cache_data
def load_data():
    try:
        return pd.read_csv("stargazing_data.csv")
    except:
        return None

df_dark = load_data()

# ---------------------------------------------------------
# 화면 1: 인트로 (PROJECT NIGHTFALL)
# ---------------------------------------------------------
if st.session_state.page == 'intro':
    st.markdown('<h1 class="main-title">PROJECT <span class="gold">NIGHTFALL</span></h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px; color:#94a3b8; margin-bottom: 50px;'>인공 지능 기반 글로벌 밤하늘 관측 적정도 분석 플랫폼</p>", unsafe_allow_html=True)
    
    if st.button("탐사 시작 (LAUNCH)"):
        st.session_state.page = 'input'
        st.rerun()

# ---------------------------------------------------------
# 화면 2: 망원경 렌즈 및 좌표 입력
# ---------------------------------------------------------
elif st.session_state.page == 'input':
    # 망원경 렌즈 효과 시각화
    st.markdown(f"""
        <div class="telescope-lens">
            <img src="http://googleusercontent.com/image_collection/image_retrieval/14254319058951770632" style="width:110%; height:110%; object-fit:cover; opacity:0.8;">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:#fbbf24;'>TARGET COORDINATES</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:40px;'>망원경을 정렬할 지점의 위도와 경도를 입력하십시오.</p>", unsafe_allow_html=True)

    # 입력 폼 중앙 밸런스 배치
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1.2])
    with c2:
        lat = st.number_input("Latitude (위도)", value=37.5, step=0.01, format="%.4f")
    with c3:
        lon = st.number_input("Longitude (경도)", value=127.0, step=0.01, format="%.4f")
    
    if st.button("좌표 고정 (ANALYZE)"):
        with st.spinner("은하수 관측 가능 여부를 계산 중입니다..."):
            time.sleep(1.2)
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.page = 'result'
            st.rerun()

# ---------------------------------------------------------
# 화면 3: 분석 결과 및 지도 시각화
# ---------------------------------------------------------
elif st.session_state.page == 'result':
    lat, lon = st.session_state.lat, st.session_state.lon
    
    st.markdown(f"### <span class='gold'>ANALYSIS RESULT:</span> TARGET [{lat}, {lon}]", unsafe_allow_html=True)
    
    # 분석 수치 대시보드 및 용어 설명
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Sky Clarity (대기 투명도)", "82%", "맑음")
        st.caption("공기 중 먼지나 습기가 적어 별빛이 얼마나 잘 뚫고 들어오는지를 나타냅니다.")
    with col_m2:
        st.metric("Bortle Scale (광공해 등급)", "Class 4", "Good")
        st.caption("인공 조명의 밝기 등급(1~9)입니다. 4등급은 은하수를 볼 수 있는 수준입니다.")
    with col_m3:
        st.metric("Visibility Prob. (관측 확률)", "Optimal", "High")
        st.caption("날씨와 광공해를 종합했을 때, 별을 성공적으로 볼 수 있는 확률입니다.")
    
    st.markdown("---")
    
    st.subheader("🗺️ 지역별 관측 품질 분포 및 타겟 지점")
    
    # 다크 테마와 어울리는 지도 타일 적용
    m = folium.Map(location=[lat, lon], zoom_start=8, tiles='cartodb dark_matter')
    
    if df_dark is not None:
        lat_c = '위도' if '위도' in df_dark.columns else 'Latitude'
        lon_c = '경도' if '경도' in df_dark.columns else 'Longitude'
        
        sample = df_dark.sample(min(2000, len(df_dark)), random_state=42)
        colors = {0: 'red', 1: 'blue', 2: 'green'}
        
        for _, row in sample.iterrows():
            folium.CircleMarker(
                location=[row[lat_c], row[lon_c]],
                radius=2.5,
                color=colors.get(row['cluster'], 'gray'),
                fill=True,
                fill_opacity=0.5,
                popup=f"Cluster: {row['cluster']}"
            ).add_to(m)

    folium.Marker(
        location=[lat, lon],
        popup="탐사 목표 지점",
        icon=folium.Icon(color='black', icon='star')
    ).add_to(m)

    # 지도가 움직여도 깜박이지 않게 고유 키 지정
    st_folium(m, use_container_width=True, height=550, key="stargazing_map_main")
    
    if st.button("다른 좌표 탐색 (RESET)"):
        st.session_state.page = 'intro'
        st.rerun()
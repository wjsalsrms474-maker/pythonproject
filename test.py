import base64
import os
import streamlit as st

# 배경 이미지 불러오기 함수
def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="한 달 치 정산 가계부", layout="centered")

# ==========================================
# 배경 이미지 설정
# ==========================================
if os.path.exists('bg.png'):
    try:
        encoded_img = get_base64_img('bg.png')
        css_code = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.80), rgba(255, 255, 255, 0.92)), url("data:image/png;base64,{encoded_img}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css_code, unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"배경 처리 오류: {e}")

# ==========================================
# 데이터 처리 로직 (Session State 사용)
# ==========================================
if "app_data" not in st.session_state:
    st.session_state.app_data = {"toss_money": {}, "history": []}

app_data = st.session_state.app_data

st.title("📱 한 달 치 정산 가계부 (웹 버전)")
st.caption("전민근식 정산 귀찮은 인간들을 위한 정산용 웹앱.")
st.divider()

if st.button("🚨 장부 전체 초기화"):
    st.session_state.app_data = {"toss_money": {}, "history": []}
    st.rerun()

st.subheader("📝 새로운 약속 입력")
date = st.text_input("날짜", placeholder="예: 5/29")
place = st.text_input("장소", placeholder="예: 술집")
price_str = st.text_input("총 지출 금액 (숫자)", placeholder="60000")
friends_str = st.text_input("참여 친구 (띄어쓰기 구분)", placeholder="이승민 이상윤")

if st.button("➕ 추가"):
    if not all([date, place, price_str, friends_str]):
        st.warning("⚠️ 모든 칸을 입력해 주세요.")
    else:
        try:
            total_price = int(price_str)
            friends = friends_str.split()
            total_people = len(friends) + 1
            dutch_pay = total_price // total_people
            
            for friend in friends:
                if friend not in st.session_state.app_data["toss_money"]:
                    st.session_state.app_data["toss_money"][friend] = 0
                st.session_state.app_data["toss_money"][friend] += dutch_pay
                
            st.session_state.app_data["history"].append({
                "date": date, "place": place, "total_price": total_price,
                "friends": friends, "dutch_pay": dutch_pay
            })
            st.success("추가 완료!")
            st.rerun()
        except ValueError:
            st.error("❌ 금액은 숫자로 입력하세요.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("💰 사람별 정산")
    if not st.session_state.app_data["toss_money"]:
        st.info("내역 없음")
    else:
        for name, money in st.session_state.app_data["toss_money"].items():
            st.metric(label=f"{name} 님이 줄 돈", value=f"{money:,} 원")

with col2:
    st.subheader("📋 상세 내역")
    for h in reversed(st.session_state.app_data["history"]):
        st.markdown(f"**{h['date']} | {h['place']}**")
        st.text(f"인당: {h['dutch_pay']:,}원")
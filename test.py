import base64
import json
import os
import streamlit as st

FILE_NAME = "settlement_data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"toss_money": {}, "history": []}

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="한 달 치 정산 가계부", layout="centered")

# ==========================================
# 워터마크 배경화면 직접 주입 방식 (linear-gradient)
# ==========================================
if os.path.exists('bg.png'):
    try:
        encoded_img = get_base64_img('bg.png')
        
        # rgba(255, 255, 255, 0.92)는 하얀색을 92% 농도로 덮는다는 뜻입니다. 
        # 사진이 너무 흐리다면 0.92를 0.85 정도로 낮추면 훨씬 선명해집니다.
        css_code = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.80), rgba(255, 255, 255, 0.92)), url("data:image/png;base64,{encoded_img}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        </style>
        """
        st.markdown(css_code, unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"배경 처리 오류: {e}")
else:
    st.info("안내: 'bg.png' 파일이 있어야 배경 워터마크가 작동합니다.")
# ==========================================

if "app_data" not in st.session_state:
    st.session_state.app_data = load_data()

app_data = st.session_state.app_data

st.title("📱 한 달 치 정산 가계부 (웹 버전)")
st.caption("전민근식 정산 귀찮은 인간들을 위한 정산용 웹앱")
st.divider()

if st.button("🚨 이번 달 장부 전체 초기화"):
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    st.session_state.app_data = {"toss_money": {}, "history": []}
    save_data(st.session_state.app_data)
    st.success("모든 장부 데이터가 초기화되었습니다.")
    st.rerun()

st.subheader("📝 새로운 약속 입력")
date = st.text_input("날짜 입력", placeholder="예: 5/29")
place = st.text_input("지출 장소 입력", placeholder="예: 1차 술집, 노래방")
price_str = st.text_input("총 지출 금액 (숫자만 입력)", placeholder="예: 60000")
friends_str = st.text_input("참여 친구 이름 (띄어쓰기로 구분)", placeholder="예: 이승민 이상윤")

if st.button("➕ 장부에 누적 추가하기"):
    if not date or not place or not price_str or not friends_str:
        st.warning("⚠️ 모든 칸을 빠짐없이 입력해 주세요.")
    else:
        try:
            total_price = int(price_str)
            friends = friends_str.split()
            
            total_people = len(friends) + 1
            dutch_pay = total_price // total_people
            
            for friend in friends:
                if friend not in app_data["toss_money"]:
                    app_data["toss_money"][friend] = 0
                app_data["toss_money"][friend] += dutch_pay
                
            event_record = {
                "date": date,
                "place": place,
                "total_price": total_price,
                "friends": friends,
                "dutch_pay": dutch_pay
            }
            app_data["history"].append(event_record)
            
            save_data(app_data)
            st.session_state.app_data = app_data
            
            st.success(f"🎉 [{place}] 장부가 안전하게 누적되었습니다! (1인당 {dutch_pay:,}원)")
            st.rerun()
            
        except ValueError:
            st.error("❌ 금액에는 숫자만 입력할 수 있습니다.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 사람별 최종 정산")
    if not app_data["toss_money"]:
        st.info("기록된 정산 내역이 없습니다.")
    else:
        for name, money in app_data["toss_money"].items():
            st.metric(label=f"{name} 님이 나에게 줄 돈", value=f"{money:,} 원")

with col2:
    st.subheader("📋 약속별 상세 내역서")
    if not app_data["history"]:
        st.info("기록된 상세 약속이 없습니다.")
    else:
        for i, h in enumerate(reversed(app_data["history"]), 1):
            st.markdown(f"**[{i}] {h['date']} | {h.get('place', '미지정')}**")
            st.text(f"• 총 금액: {h['total_price']:,} 원")
            st.text(f"• 참여자: {', '.join(h['friends'])}")
            st.text(f"• 인당 배정: {h['dutch_pay']:,} 원")
            st.markdown("---")
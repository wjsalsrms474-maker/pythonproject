import streamlit as st

st.set_page_config(page_title="한 달 치 정산 가계부", layout="centered")

# 세션 상태 초기화 (데이터가 메모리에만 저장됨)
if "app_data" not in st.session_state:
    st.session_state.app_data = {"toss_money": {}, "history": []}

app_data = st.session_state.app_data

st.title("📱 한 달 치 정산 가계부 (웹 버전)")
st.caption("개인용: 입력 내용이 새로고침 시 초기화됩니다.")
st.divider()

# 초기화 버튼
if st.button("🚨 장부 전체 초기화"):
    st.session_state.app_data = {"toss_money": {}, "history": []}
    st.rerun()

st.subheader("📝 새로운 약속 입력")
date = st.text_input("날짜", placeholder="예: 5/29")
place = st.text_input("장소", placeholder="예: 술집")
price_str = st.text_input("총 지출 금액 (숫자)", placeholder="60000")
friends_str = st.text_input("참여 친구 (띄어쓰기로 구분)", placeholder="이승민 이상윤")

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
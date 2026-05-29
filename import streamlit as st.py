import streamlit as st

# 웹사이트 제목 설정
st.title("📱 모바일 정산 가계부 (웹 버전)")

# 간단한 문구 출력
st.write("우리들만의 한 달 치 정산 웹사이트가 성공적으로 개설되었습니다!")

# 마우스로 입력하는 칸 테스트
name = st.text_input("당신의 이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, {name} 님 고생하시네요")
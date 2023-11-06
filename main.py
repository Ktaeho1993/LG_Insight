import streamlit as st
import LG_Insight, LG_Insight_model

PAGES = {
    "데이터 전처리": LG_Insight,
    "예측 모델 학습": LG_Insight_model

}

st.sidebar.title('선택창')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

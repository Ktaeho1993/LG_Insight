import streamlit as st
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from model import MRF_model
import time

# 페이지 설정
st.set_page_config(page_title='LG Insight Model Training')

def app():
    st.title("LG 전자 모델 학습")

    def load_data(file):
        data = pd.read_csv(file)
        return data

    # CSV 파일을 업로드
    file = st.text_input("CSV 파일명을 입력해주세요.")
    if file:  # 파일이 업로드 되었다면
        file = file + '.csv'
        data = load_data(file)
        st.write("파일이 성공적으로 불러와졌습니다.")

        if st.button("모델 학습"):
            X_data = data[['Metering Position Set Value 3','Back Pressure Set Value 1', 'Metering RPM Set Value 1', 'Filling Process Set Position 1', 'Velocity Set Value during Filling 1', 'Velocity Set Value during Filling 2', 'VP Position Set Value','Packing Pressure Set Value 1', 
                        'Packing Time Set Value 1', 'Barrel Temperature Set Value ZH']]
            y_data_list = [
                data[['T3_Detect','T4_Detect','T6_Detect','T8_Detect','T12_Detect','T13_Detect','T14_Detect','T16_Detect']],
                data[['T3_MaxDetect','T4_MaxDetect','T6_MaxDetect','T8_MaxDetect','T12_MaxDetect','T13_MaxDetect','T14_MaxDetect','T16_MaxDetect']],
                data[['T3_Max','T4_Max','T6_Max','T8_Max','T12_Max','T13_Max','T14_Max','T16_Max']],
                data[['P1_Max','P2_Max','P3_Max','P4_Max','P5_Max']],
                data[['P1_MaxDetect','P2_MaxDetect','P3_MaxDetect','P4_MaxDetect','P5_MaxDetect']]
            ]

            # 모델 학습
            with st.spinner('모델을 학습 중입니다...'):
                models = [MRF_model() for _ in y_data_list]
                results = [model.fit(X_data, y_data) for model, y_data in zip(models, y_data_list)]
                st.success("학습이 완료되었습니다!")

            # 테스트 데이터로 예측
            y_preds = [model.predict(X_data) for model in models]

            # MAE , 소수점 둘째 자리
            maes = [mean_absolute_error(y_data, y_pred) for y_data, y_pred in zip(y_data_list, y_preds)]
            maes = [round(mae, 2) for mae in maes]

            # R^2 , 소수점 둘째 자리
            r2s = [r2_score(y_data, y_pred) for y_data, y_pred in zip(y_data_list, y_preds)]
            r2s = [round(r2, 2) for r2 in r2s]

            # 결과를 출력합니다.
            st.write(f"Mean Absolute Errors: {maes}")
            st.write(f"R2s: {r2s}")

            # MAE와 R2 막대 그래프
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            colors = ['b', 'g', 'r', 'c', 'm']
            labels = ['T_Detect', 'T_Max', 'T_MaxDetect', 'P_Max', 'P_MaxDetect']

            # MAE 막대 그래프
            ax1.bar(labels, maes, color=colors)
            ax1.set_xlabel('Predict Values')
            ax1.set_ylabel('MAE')
            ax1.set_title('MAE RESULT')
            for index, value in enumerate(maes):
                ax1.text(index, value, str(value))

            # R2 막대 그래프
            ax2.bar(labels, r2s, color=colors)
            ax2.set_xlabel('Predict Values')
            ax2.set_ylabel('R2')
            ax2.set_title('R2 RESULT')
            for index, value in enumerate(r2s):
                ax2.text(index, value, str(value))

            st.pyplot(fig)

            

if __name__ == '__main__':
    app()

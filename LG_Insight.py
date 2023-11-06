import streamlit as st
import pandas as pd
import numpy as np

def app():
    st.title("데이터 전처리")
    
    # 파일 업로드를 위한 함수
    uploaded_file = st.file_uploader("여기에 csv 파일을 업로드해주세요.", type=['csv'])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        
        X_data = data[['Metering Position Set Value 3','Back Pressure Set Value 1', 'Metering RPM Set Value 1', 'Filling Process Set Position 1', 'Velocity Set Value during Filling 1', 'Velocity Set Value during Filling 2', 'VP Position Set Value','Packing Pressure Set Value 1', 
                    'Packing Time Set Value 1', 'Barrel Temperature Set Value ZH']]
        y_data = data[['T3_Detect','T4_Detect','T6_Detect','T8_Detect','T12_Detect','T13_Detect','T14_Detect','T16_Detect','T3_Max','T4_Max','T6_Max','T8_Max','T12_Max','T13_Max','T14_Max','T16_Max',
                    'T3_MaxDetect','T4_MaxDetect','T6_MaxDetect','T8_MaxDetect','T12_MaxDetect','T13_MaxDetect','T14_MaxDetect','T16_MaxDetect','P1_Max','P2_Max','P3_Max','P4_Max','P5_Max','P1_MaxDetect','P2_MaxDetect','P3_MaxDetect','P4_MaxDetect', 'P5_MaxDetect']]
        if st.button('데이터 전처리'):
            
            # 일단 0값있으면 다 삭제하는 전처리
            combined_data = pd.concat([X_data, y_data], axis=1)
            combined_data = combined_data.loc[~(combined_data==0).any(axis=1)]
        
            # 전처리된거 _pre 삽입
            new_filename = uploaded_file.name.split('.')[0] + '_pre.csv'
        
            # 데이터를 새로운 파일로 저장
            combined_data.to_csv(new_filename, index=False)
            st.write("0 값을 가진 행이 삭제된 데이터:")
            st.dataframe(combined_data)
            
        if st.button('변수나누기'):
            # 가로출력하기
            col1, col2 = st.beta_columns(2)
            with col1:
                st.write("X_data:")
                st.dataframe(X_data)
            with col2:
                st.write("y_data:")
                st.dataframe(y_data)
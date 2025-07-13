import streamlit as st
import pandas as pd
import plotly.express as px # 인터랙티브 그래프를 위해 Plotly 사용

st.title("💡 광도 변화 곡선 분석기")

st.markdown("""
이 앱은 CSV 파일로부터 광도 변화 데이터를 읽어들여 그래프로 시각화합니다.
시간과 밝기(또는 확대율) 데이터를 포함하는 CSV 파일을 업로드해주세요.
""")

uploaded_file = st.file_uploader("CSV 파일을 선택해주세요", type="csv")

if uploaded_file is not None:
    try:
        # CSV 파일 읽기
        df = pd.read_csv(uploaded_file)

        # 사용자가 어떤 컬럼이 '시간'이고 어떤 컬럼이 '밝기'인지 선택하도록 함
        st.subheader("데이터 컬럼 선택")
        col1, col2 = st.columns(2)
        with col1:
            time_col = st.selectbox("시간 데이터 컬럼을 선택하세요:", df.columns)
        with col2:
            brightness_col = st.selectbox("밝기(광도/확대율) 데이터 컬럼을 선택하세요:", df.columns)

        if time_col and brightness_col:
            st.subheader("업로드된 데이터 미리보기")
            st.dataframe(df.head())

            st.subheader("광도 변화 곡선")
            fig = px.line(df, x=time_col, y=brightness_col,
                          title=f'광도 곡선 ({brightness_col} vs {time_col})',
                          labels={time_col: '시간', brightness_col: '밝기'},
                          template="plotly_dark") # 어두운 테마
            fig.update_traces(line_color='lime') # 라인 색상 변경
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("간단한 데이터 분석")
            st.write(f"**최대 밝기:** {df[brightness_col].max():.3f}")
            st.write(f"**최소 밝기:** {df[brightness_col].min():.3f}")
            st.write(f"**평균 밝기:** {df[brightness_col].mean():.3f}")
            st.write(f"**데이터 포인트 수:** {len(df)}")

            # 추가적인 간단한 '해석' 기능 예시: 피크 지점 강조
            # 실제 미세중력렌즈 피크 감지는 더 복잡한 알고리즘 필요
            # 여기서는 단순히 최대값 지점을 표시하는 예시
            max_brightness_time = df.loc[df[brightness_col].idxmax(), time_col]
            st.write(f"**가장 밝았던 시간:** {max_brightness_time}")

    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
        st.info("올바른 CSV 형식인지 확인하거나, 시간 및 밝기 컬럼을 정확히 지정해주세요.")

import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

st.set_page_config(page_title="USDJPY Air Gauge", layout="centered")

st.title("USDJPY 空気温度計")

keyword = st.text_input("キーワード", "US CPI")

pytrends = TrendReq(hl="en-US", tz=360)

try:
    pytrends.build_payload([keyword], timeframe="today 1-m", geo="US")
    data = pytrends.interest_over_time()

    if data.empty:
        st.warning("データが取得できませんでした")
    else:
        today = data[keyword].iloc[-1]
        avg_7 = data[keyword].iloc[-7:].mean()
        ratio = today / avg_7 if avg_7 != 0 else 0

        if ratio >= 2:
            color = "🔴 RED（激アツ）"
            bg = "#ff4d4d"
        elif ratio >= 1.5:
            color = "🟡 YELLOW（注視）"
            bg = "#ffcc00"
        else:
            color = "🟢 GREEN（通常）"
            bg = "#2e7d32"

        st.markdown(
            f"""
            <div style="background-color:{bg};padding:30px;border-radius:15px;text-align:center;">
                <h2>今日の検索値: {today}</h2>
                <h3>7日平均: {avg_7:.2f}</h3>
                <h3>倍率: {ratio:.2f}</h3>
                <h1>{color}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

except Exception as e:
    st.error(f"エラーが発生しました: {e}")

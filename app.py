import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

st.set_page_config(page_title="USDJPY Air Gauge", layout="centered")

st.title("USDJPY 空気温度計")

keyword = st.text_input("キーワード", "US CPI")

pytrends = TrendReq(hl='en-US', tz=360)

try:
    pytrends.build_payload([keyword], timeframe='today 1-m', geo='US')
    data = pytrends.interest_over_time()

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
        <div style="padding:30px; background:{bg}; color:white; border-radius:15px;">
        <h3>{keyword}</h3>
        <p>今日の検索値: <b>{today}</b></p>
        <p>7日平均: <b>{round(avg_7,2)}</b></p>
        <p>倍率: <b>{round(ratio,2)}</b></p>
        <h1 style="font-size:40px;">{color}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

except Exception as e:
    st.error("データ取得に失敗しました")
    st.write(e)

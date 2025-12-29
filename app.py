import streamlit as st
import pandas as pd

# 1. 設定網頁標題
st.set_page_config(page_title="影片搜尋神器", page_icon="📺")
st.title("📺 內部維修影片搜尋")

# 2. 讀取檔案 (特別針對你的無標題 CSV 設定)
@st.cache_data
def load_data():
    # header=None 代表檔案沒有標題，我們自己補上 Title 和 URL
    df = pd.read_csv("影片清單.csv", header=None, names=["Title", "URL"])
    return df

try:
    df = load_data()
    
    # 3. 搜尋功能
    search = st.text_input("🔍 請輸入關鍵字 (例如：更換、WST...)", "")

    # 4. 顯示結果
    if search:
        # 搜尋邏輯：只要標題裡面有包含關鍵字就抓出來
        results = df[df['Title'].str.contains(search, case=False)]
        st.success(f"找到 {len(results)} 個相關影片：")
    else:
        # 如果沒搜尋，預設顯示前 10 筆就好，避免畫面太長
        st.info("請輸入關鍵字開始搜尋，下方顯示最新 5 筆範例：")
        results = df.head(5)

    # 5. 列表顯示
    for index, row in results.iterrows():
        with st.expander(f"▶️ {row['Title']}"): # 做成摺疊選單比較整齊
            st.write(f"影片連結: {row['URL']}")
            try:
                st.video(row['URL'])
            except:
                st.error("無法載入影片，請點擊連結觀看")

except FileNotFoundError:
    st.error("❌ 找不到檔案！請確認 '影片清單.csv' 跟 app.py 在同一個資料夾內。")
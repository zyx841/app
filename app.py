import streamlit as st
import pandas as pd

# --- 1. 設定頁面 (手機版面優化) ---
st.set_page_config(page_title="千山淨水維修", page_icon="📱", layout="centered")

# CSS 美化：把按鈕變大，好按一點
st.markdown("""
    <style>
    .stVideo {width: 100% !important;}
    .stButton>button {
        width: 100%;
        margin-top: 20px;
        background-color: #f0f2f6;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 千山淨水維修")

# --- 2. 讀取資料 ---
@st.cache_data
def load_data():
    try:
        # header=None 代表檔案沒有標題，我們自己補上 Title 和 URL
        df = pd.read_csv("影片清單.csv", header=None, names=["Title", "URL"])
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- 3. 初始化 Session State (用來紀錄目前看到第幾筆) ---
if 'limit' not in st.session_state:
    st.session_state.limit = 10  # 一開始只顯示 10 筆，避免手機當機

# --- 4. 搜尋功能 ---
search_query = st.text_input("🔍 搜尋影片...", placeholder="輸入關鍵字 (例如：更換、WST...)")

# --- 5. 篩選與顯示邏輯 ---
if not df.empty:
    if search_query:
        # 【有搜尋時】：顯示所有符合的結果 (不用分頁，因為通常搜尋結果不多)
        filtered_df = df[df['Title'].str.contains(search_query, case=False)]
        st.success(f"找到 {len(filtered_df)} 個相關影片")
        
        for index, row in filtered_df.iterrows():
            st.markdown("---")
            st.write(f"**{row['Title']}**")
            try:
                st.video(row['URL'])
            except:
                st.write(f"連結: {row['URL']}")
    else:
        # 【沒搜尋時】：顯示「無限清單」模式
        st.caption("滑動瀏覽所有影片")
        
        # 只取出目前 limit 數量的影片
        display_df = df.iloc[:st.session_state.limit]
        
        for index, row in display_df.iterrows():
            st.markdown("---")
            st.subheader(f"{index+1}. {row['Title']}") # 加上編號
            try:
                st.video(row['URL'])
            except:
                st.write(f"連結: {row['URL']}")
        
        # --- 載入更多按鈕 ---
        # 如果目前顯示的數量還小於總數，就顯示按鈕
        if st.session_state.limit < len(df):
            if st.button("👇 點我載入更多影片 (+10)"):
                st.session_state.limit += 10
                st.rerun() # 重新整理畫面
            
            st.caption(f"目前顯示 {st.session_state.limit} / {len(df)} 筆")

else:
    st.error("找不到 '影片清單.csv'，請確認檔案已上傳。")

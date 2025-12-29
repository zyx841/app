import streamlit as st
import pandas as pd

# --- 1. 設定頁面 ---
st.set_page_config(page_title="千山淨水維修", page_icon="🛠️", layout="centered")

# CSS 美化：
# 1. 讓摺疊選單標題變大
# 2. 讓外部連結看起來像按鈕一樣明顯
st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
    }
    a.external-link {
        display: inline-block;
        padding: 10px 20px;
        background-color: #FF0000;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ 千山淨水維修")

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

# --- 3. 初始化 Session State (紀錄目前看到第幾筆) ---
if 'limit' not in st.session_state:
    st.session_state.limit = 20

# --- 4. 搜尋功能 ---
search_query = st.text_input("🔍 搜尋影片...", placeholder="輸入關鍵字 (例如：更換、WST...)")

# --- 5. 顯示邏輯 ---
if not df.empty:
    
    # 準備顯示資料
    if search_query:
        # 有搜尋：顯示全部符合結果
        display_df = df[df['Title'].str.contains(search_query, case=False)]
        st.success(f"找到 {len(display_df)} 個相關影片")
    else:
        # 沒搜尋：只顯示前 N 筆
        st.caption("點擊標題展開，若無法播放請點擊下方連結 👇")
        display_df = df.iloc[:st.session_state.limit]

    # --- 核心顯示區塊 ---
    for index, row in display_df.iterrows():
        with st.expander(f"📄 {row['Title']}"):
            
            # 1. 嘗試顯示播放器
            try:
                st.video(row['URL'])
            except:
                st.warning("⚠️ 預覽載入失敗")

            # 2. 【新增】不管能不能播，都附上超連結
            # 這裡做了一個點擊會跳轉的文字連結
            st.markdown(f"**👉 [點擊前往 YouTube 觀看]({row['URL']})**")
            
            # 如果想要顯示原始連結網址，可以把下面這行打開
            # st.caption(f"網址: {row['URL']}")

    # --- 載入更多按鈕 ---
    if not search_query and st.session_state.limit < len(df):
        st.markdown("---")
        if st.button("👇 載入更多影片 (+20)"):
            st.session_state.limit += 20
            st.rerun()
            
else:
    st.error("找不到 '影片清單.csv'，請確認檔案已上傳。")

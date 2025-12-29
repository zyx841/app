import streamlit as st
import pandas as pd

# --- 1. 設定頁面 ---
st.set_page_config(page_title="千山淨水維修", page_icon="🛠️", layout="centered")

# CSS 美化：讓摺疊選單的字大一點，比較好點
st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ 千山淨水維修影片庫")

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
    st.session_state.limit = 20  # 因為現在是純文字，比較不吃資源，一次顯示 20 筆也沒問題

# --- 4. 搜尋功能 (置頂) ---
search_query = st.text_input("🔍 搜尋影片...", placeholder="輸入關鍵字 (例如：更換、WST...)")

# --- 5. 顯示邏輯 (摺疊選單版) ---
if not df.empty:
    
    # 準備要顯示的資料
    if search_query:
        # 有搜尋時：顯示所有符合結果
        display_df = df[df['Title'].str.contains(search_query, case=False)]
        st.success(f"找到 {len(display_df)} 個相關影片")
    else:
        # 沒搜尋時：只顯示前 N 筆 (避免網頁卡住)
        st.caption("點擊標題即可展開觀看影片 👇")
        display_df = df.iloc[:st.session_state.limit]

    # --- 核心修改：改用 Expander (下拉摺疊) ---
    for index, row in display_df.iterrows():
        # 這裡就是你要的「點進下拉式選單」效果
        with st.expander(f"📄 {row['Title']}"): 
            try:
                st.video(row['URL'])
            except:
                st.write(f"🔗 影片連結: {row['URL']}")

    # --- 載入更多按鈕 (只有在沒搜尋時顯示) ---
    if not search_query and st.session_state.limit < len(df):
        st.markdown("---")
        if st.button("👇 載入更多影片 (+20)"):
            st.session_state.limit += 20
            st.rerun()
            
else:
    st.error("找不到 '影片清單.csv'，請確認檔案已上傳。")

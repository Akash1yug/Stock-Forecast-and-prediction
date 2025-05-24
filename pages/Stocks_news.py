import streamlit as st
import requests
from datetime import datetime

# ------------- SETUP ----------------
st.set_page_config(page_title="📈 Stock Market News", layout="wide")

# 🔧 API KEY
NEWS_API_KEY = "c0f257efc633427eb8f3766f9eb3c0cb"  # Replace with your NewsAPI key

# ------------- PAGE HEADER -------------
st.markdown("""
    <style>
    .main-title {
        font-size:40px; font-weight:700; color:#0e76a8;
    }
    .news-card {
        background-color: #f8f9fa;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📢 Stock Market News Dashboard</div>', unsafe_allow_html=True)
st.markdown("Real-time financial and stock market news updates.")

# ------------- SIDEBAR ---------------
with st.sidebar:
    st.header("🔍 Filter News")
    topic = st.text_input("Enter company or topic", value="stock market")
    count = st.slider("Number of articles", 3, 20, 8)
    sort_option = st.selectbox("Sort by", ["publishedAt", "popularity", "relevancy"])
    st.markdown("---")
    st.markdown("Powered by [NewsAPI.org](https://newsapi.org)")

# ------------- FETCH NEWS FUNCTION -------------
def fetch_news(query, sort_by, count, api_key):
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&sortBy={sort_by}&language=en&pageSize={count}&apiKey={api_key}"
    )
    response = requests.get(url)
    return response.json()

# ------------- FETCH & DISPLAY -------------
news_data = fetch_news(topic, sort_option, count, NEWS_API_KEY)

if news_data.get("status") == "ok" and news_data["articles"]:
    for article in news_data["articles"]:
        title = article["title"]
        description = article.get("description", "No description available.")
        url = article["url"]
        source = article["source"]["name"]
        date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y")

        st.markdown(f"""
            <div class="news-card">
                <h4>📰 {title}</h4>
                <p>{description}</p>
                <p><b>Source:</b> {source} | 🗓️ <i>{date}</i></p>
                <a href="{url}" target="_blank">🔗 Read Full Article</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("❌ No news found. Try a different topic or keyword.")


st.write("")
st.markdown(
    ":gray[✨ Made with ❤️ and passion by **Akash**. ©2025 [theyug.com](https://theyug.com) - All Rights Reserved.]"
)
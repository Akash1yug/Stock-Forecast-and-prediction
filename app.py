import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = "heavy_dollar_sign:",
    layout = "wide"
)

st.title("Trading Guide App :bar_chart:")
st.header("We provide trading platfrom, for Analysis and Prediction of Stock Market")
st.image("image1.jpg")

# About Me Section
st.subheader("About Me")
st.markdown("""
Hi, I'm **Akash Kumar** — a passionate **Python programmer**, creative **artist**, curious **tech enthusiast**, and a dedicated **trader**.  
I'm also deeply fascinated by the mysteries of **outer space**.  
I love blending logic with creativity, whether it's coding, sketching, or exploring the cosmos.
""")

st.write("")
st.markdown(
    ":gray[✨ Made with ❤️ and passion by **Akash**. ©2025 [theyug.com](https://theyug.com) - All Rights Reserved.]"
)

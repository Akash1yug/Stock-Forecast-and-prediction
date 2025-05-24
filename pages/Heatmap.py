import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import date
import numpy as np


@st.cache_data(ttl=300)
def get_index_details(category):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Upgrade-Insecure-Requests': "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8",
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    category = category.upper().replace('&', '%26').replace(' ', '%20')

    try:
        ref_url = f"https://www.nseindia.com/market-data/live-equity-market?symbol={category}"
        ref = requests.get(ref_url, headers=headers)
        url = f"https://www.nseindia.com/api/equity-stockIndices?index={category}"
        data = requests.get(url, headers=headers, cookies=ref.cookies.get_dict()).json()
        df = pd.DataFrame(data['data'])
        if not df.empty:
            df = df.drop(["meta"], axis=1)
            df = df.set_index("symbol", drop=True)
            df['ffmc'] = round(df['ffmc']/10000000, 0)
            df = df.iloc[1:].reset_index(drop=False)
        return df
    except Exception as e:
        print("Error Fetching Index Data from NSE. Aborting....")
        return pd.DataFrame()

index_list = [
    'NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100', 'NIFTY MIDCAP 150',
    'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100', 'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100',
    'NIFTY 200', 'NIFTY AUTO', 'NIFTY BANK', 'NIFTY ENERGY', 'NIFTY FINANCIAL SERVICES',
    'NIFTY FINANCIAL SERVICES 25/50', 'NIFTY FMCG', 'NIFTY IT', 'NIFTY MEDIA', 'NIFTY METAL',
    'NIFTY PHARMA', 'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY PRIVATE BANK', 'Securities in F&O',
    'Permitted to Trade', 'NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30',
    'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30', 'NIFTY ALPHA 50',
    'NIFTY200 QUALITY 30', 'NIFTY ALPHA LOW-VOLATILITY 30', 'NIFTY200 MOMENTUM 30', 'NIFTY COMMODITIES',
    'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE', 'NIFTY MNC', 'NIFTY GROWTH SECTORS 15',
    'NIFTY PSE', 'NIFTY SERVICES SECTOR', 'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15'
]

pd.set_option("display.max_rows", None, "display.max_columns", None)

st.set_page_config(
    page_title='📊 NSE Heatmap Dashboard',
    layout="centered")

st.markdown(
    f"""
    <style>
      .stAppViewContainer .stMain .stMainBlockContainer{{ max-width: 1440px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

header1, header2 = st.columns([3, 1])
with header1:
    st.subheader("📈 NSE Indices Heatmap - Visualizer")
    col1, col2, _ = st.columns([2, 1, 1])
    index_filter = col1.selectbox("📊 Choose Index", index_list, index=0)
    slice_by = col2.selectbox("🎯 Slice By", ["Market Cap", "Gainers", "Losers", "All"], index=0)

with header2:
    df = get_index_details(index_filter)

    advances = df[df['pChange'] > 0].shape[0]
    declines = df[df['pChange'] < 0].shape[0]
    no_change = df[df['pChange'] == 0].shape[0]

    fig = px.pie(
        names=['Advances', 'Declines', 'No Change'],
        values=[advances, declines, no_change],
        color=['Advances', 'Declines', 'No Change'],
        color_discrete_map={
            'Advances': '#2ecc71',
            'Declines': '#e74c3c',
            'No Change': '#95a5a6'
        }
    )

    fig.update_traces(hole=0.7, textinfo='none')
    fig.update_layout(
        width=220,
        height=220,
        showlegend=False,
        annotations=[dict(
            text=f'<b>{advances}<br>Up<br><br>{declines}<br>Down<b>',
            x=0.5, y=0.5, font_size=20, showarrow=False
        )],
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig)

if not df.empty:

    if slice_by == 'Market Cap':
        slice_factor = 'ffmc'
        color = 'pChange'
        color_scale = 'RdYlGn'
    elif slice_by == 'Gainers':
        slice_factor = 'pChange'
        color = 'pChange'
        color_scale = 'RdYlGn'
    elif slice_by == 'Losers':
        df = df[df["pChange"] < 0]
        df['Abs'] = df['pChange'].abs()
        slice_factor = 'Abs'
        color = 'pChange'
        color_scale = 'Reds'  # or ['white', '#ff7a3a']


    st.divider()



    # Define min and max for uniform color scaling
    color_min = -5
    color_max = 5

    fig = px.treemap(
        df,
        path=['symbol'],
        values=slice_factor,
        color=color,
        color_continuous_scale=[(0.0, "red"), (0.5, "white"), (1.0, "green")],
        range_color=[color_min, color_max],
        custom_data=['pChange']
    )


    fig.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
        width=350,
        height=700,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)"
    )

    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Size: %{value}<br>Change: %{customdata[0]:.2f}%',
        texttemplate='%{label}<br>%{customdata[0]:.2f}%',
        textposition='middle center'
    )

    fig.update_coloraxes(showscale=False)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Failed to fetch data. Please try again later.")

st.write("")
st.markdown(
    ":gray[✨ Made with ❤️ and passion by **Akash**. ©2025 [theyug.com](https://theyug.com) - All Rights Reserved.]"
)

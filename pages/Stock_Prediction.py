import streamlit as st
from pages.utils.model_train import get_data, stationary_check, get_rolling_mean, get_differncing_order, fit_model, evaluate_model, scaling, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast
import datetime
import ta
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
     page_title="Stock Prediction",
     page_icon="chart_with_upwards_trend",
     layout="wide",
    )
st.title("Stock Prediction")


col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Enter the Stock Symbol", "TSLA")

with col2:
    start_date = st.date_input("Start Date", datetime.date(today.year - 1, today.month, today.day))

with col3:
    end_date = st.date_input("End Date", datetime.date(today.year, today.month, today.day))

    data = yf.download(ticker, start=start_date, end=end_date)

st.subheader("Predicting Next 30 days Close Price for:"+ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differncing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**",rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

st.write("##### FORECAST DATA (Next 30 days)")

fig_tail = plotly_table(forecast.sort_index(ascending = True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])



st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)


st.write("")
st.markdown(
    ":gray[✨ Made with ❤️ and passion by **Akash**. ©2025 [theyug.com](https://theyug.com) - All Rights Reserved.]"
)
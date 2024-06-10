import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Function to load real-time data
def load_data(coin, start_date, end_date):
    try:
        df = yf.download(coin, start=start_date, end=end_date, interval='1d')
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")

# Function to display line chart
def display_line_chart(df, coin):
    fig_line = px.line(df, x=df.index, y='Close', title=f'{coin} Price Trend', color_discrete_sequence=['blue'])
    fig_line.update_xaxes(title='Time')
    fig_line.update_yaxes(title='Price (USD)')
    st.plotly_chart(fig_line, use_container_width=True)

# Function to display moving average chart
def display_ma_chart(df, coin):
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='green')))
    fig_ma.add_trace(go.Scatter(x=df.index, y=df['MA_30'], mode='lines', name='Moving Average (30 days)', line=dict(color='red')))
    fig_ma.update_layout(title=f'{coin} Moving Average (30 days)', xaxis_title='Time', yaxis_title='Price (USD)')
    st.plotly_chart(fig_ma, use_container_width=True)

# Function to display histogram of daily returns
def display_histogram(df, coin):
    daily_returns = df['Close'].pct_change().dropna()
    fig_histogram = px.histogram(daily_returns, x=daily_returns, nbins=50, title=f'{coin} Daily Returns Distribution')
    fig_histogram.update_xaxes(title='Daily Returns')
    fig_histogram.update_yaxes(title='Frequency')
    st.plotly_chart(fig_histogram, use_container_width=True)

# Function to display pie chart of monthly trading volume contribution
def display_pie_chart(df, coin):
    df['Month'] = df.index.month
    monthly_volume = df.groupby('Month')['Volume'].sum()
    fig_pie = px.pie(names=monthly_volume.index, values=monthly_volume.values, title=f'{coin} Monthly Trading Volume Contribution')
    st.plotly_chart(fig_pie, use_container_width=True)

def main():
    st.title('Cryptocurrency Analysis App')
    
    # Select a cryptocurrency
    coin = st.sidebar.selectbox('Select a cryptocurrency', ['BTC-USD', 'ETH-USD', 'XRP-USD'])
    
    # Set start and end dates
    start_date = pd.to_datetime('2020-04-01')
    end_date = datetime.now().date()
    
    # Load data
    data_load_state = st.text('Loading data...')
    df = load_data(coin, start_date, end_date)
    data_load_state.text('Data loading complete!')

    # Menu to choose graphs
    selected_chart = st.sidebar.selectbox('Select Chart', ['Price Trend', 'Moving Average', 'Daily Returns Histogram', 'Monthly Volume Contribution'])

    # Display selected chart
    if selected_chart == 'Price Trend':
        display_line_chart(df, coin)
    elif selected_chart == 'Moving Average':
        display_ma_chart(df, coin)
    elif selected_chart == 'Daily Returns Histogram':
        display_histogram(df, coin)
    elif selected_chart == 'Monthly Volume Contribution':
        display_pie_chart(df, coin)

    # Button to manually refresh data
    if st.button('Refresh Data'):
        data_load_state.text('Refreshing data...')
        df = load_data(coin, start_date, end_date)
        data_load_state.text('Data refreshed!')

if __name__ == '__main__':
    main()


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="NexMindAi — Book Forecast Tool", layout="wide")

# Header with logo and title
with st.container():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://raw.githubusercontent.com/Nexmindaiii/inventory-forecast-demo/main/BBEFF79C-59B9-4CFF-A669-7614FF1FE647.png", width=80)
    with col2:
        st.title("NexMindAi — Book Inventory Forecast Tool")
        st.caption("Because smart stock saves profit.")

# Upload section
st.subheader("1. Upload Your Sales Data")
uploaded_file = st.file_uploader("Upload your sales data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Your data was uploaded successfully!")
else:
    st.info("No file uploaded. Using sample data instead.")
    books = [f"Book {i}" for i in range(1, 11)]
    dates = pd.date_range(end=pd.Timestamp.today(), periods=6, freq='M')
    data = []
    np.random.seed(42)
    for book in books:
        monthly_sales = np.random.poisson(lam=np.random.randint(20, 100), size=6)
        for date, sales in zip(dates, monthly_sales):
            data.append({"Book": book, "Date": date, "Sales": sales})
    df = pd.DataFrame(data)

# Forecast section
if 'Date' in df.columns and 'Sales' in df.columns and 'Book' in df.columns:
    st.subheader("2. View Forecast")
    forecast_df = df.groupby(['Book']).tail(3).groupby('Book')['Sales'].mean().reset_index()
    forecast_df['Forecast_Next_Month'] = forecast_df['Sales'].round(0).astype(int)
    forecast_df.drop(columns='Sales', inplace=True)
    st.dataframe(forecast_df)

    st.subheader("3. Download & Analyze")
    csv = forecast_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Forecast CSV", csv, "forecast.csv", "text/csv")

    st.subheader("Example Trend: Book 1")
    if 'Book 1' in df['Book'].values:
        book1_data = df[df['Book'] == 'Book 1']
        plt.figure(figsize=(8, 4))
        plt.plot(book1_data['Date'], book1_data['Sales'], marker='o')
        plt.title("Sales Trend for Book 1")
        plt.xlabel("Month")
        plt.ylabel("Units Sold")
        plt.grid(True)
        st.pyplot(plt)
else:
    st.warning("Your file must have 'Book', 'Date', and 'Sales' columns.")

# CTA and pricing section
st.markdown("---")
st.markdown("### Ready to use NexMindAi in your business?")
st.link_button("Contact Us for a Custom Forecast", "mailto:youremail@domain.com")

st.markdown("### Plans")
st.info("**Starter (Free):** Manual CSV upload and download\n**Pro (Coming Soon):** Auto-sync, API, and priority support")

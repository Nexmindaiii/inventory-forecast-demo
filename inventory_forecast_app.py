
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="NextMind AI — Book Forecast Tool", layout="centered")

# Logo and Title
st.image("https://raw.githubusercontent.com/Nexmindaiii/inventory-forecast-demo/main/nexmind-ai-logo.jpeg", width=200)
st.title("NextMind AI — Book Inventory Forecast Tool")
st.caption("Made by NexMind AI — because smart stock saves profit.")

st.write("Upload your sales data or use sample data below to forecast next month's inventory needs.")

# Upload CSV option
uploaded_file = st.file_uploader("Upload your sales data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Your data was uploaded successfully!")
else:
    # Use sample data
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

# Forecast
if 'Date' in df.columns and 'Sales' in df.columns and 'Book' in df.columns:
    forecast_df = df.groupby(['Book']).tail(3).groupby('Book')['Sales'].mean().reset_index()
    forecast_df['Forecast_Next_Month'] = forecast_df['Sales'].round(0).astype(int)
    forecast_df.drop(columns='Sales', inplace=True)

    # Display forecast
    st.subheader("Forecast for Next Month")
    st.dataframe(forecast_df)

    # Download CSV
    csv = forecast_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Forecast CSV", csv, "forecast.csv", "text/csv")

    # Chart for one book
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

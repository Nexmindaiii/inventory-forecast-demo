
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Inventory Forecaster", layout="centered")

st.title("Book Inventory Forecast Tool")
st.write("This demo predicts next month's demand for a sample of book titles, based on the last 3 months of sales data.")

# Sample data
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
forecast_df = df.groupby(['Book']).tail(3).groupby('Book')['Sales'].mean().reset_index()
forecast_df['Forecast_Next_Month'] = forecast_df['Sales'].round(0).astype(int)
forecast_df.drop(columns='Sales', inplace=True)

# Display forecast
st.subheader("Forecast for Next Month")
st.dataframe(forecast_df)

# Plot example forecast for one book
st.subheader("Example Trend: Book 1")
book1_data = df[df['Book'] == 'Book 1']
plt.figure(figsize=(8, 4))
plt.plot(book1_data['Date'], book1_data['Sales'], marker='o')
plt.title("Sales Trend for Book 1")
plt.xlabel("Month")
plt.ylabel("Units Sold")
plt.grid(True)
st.pyplot(plt)

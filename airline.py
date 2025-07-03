import streamlit as st
import pandas as pd
import numpy as np

@st.cache(allow_output_mutation=True)
def load_data(path):
    df = pd.read_csv(path)
    df["Departure Date"] = pd.to_datetime(df["Departure Date"], errors='coerce')
    return df



def main():
    st.set_page_config(page_title="Airline Demand Analysis", layout="wide")
    st.title("🛫 Airline Booking Market Demand Dashboard")


    df = load_data("D://ip//Airline Dataset.csv")

    st.sidebar.header("🔎 Filter Options")
    

    min_date, max_date = df["Departure Date"].min(), df["Departure Date"].max()
    date_range = st.sidebar.date_input("Departure Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)


    continents = st.sidebar.multiselect("Select Continents", df["Airport Continent"].unique(), default=df["Airport Continent"].unique())


    flight_statuses = st.sidebar.multiselect("Flight Status", df["Flight Status"].unique(), default=df["Flight Status"].unique())


    genders = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())


    filtered = df[
        (df["Departure Date"] >= pd.to_datetime(date_range[0])) &
        (df["Departure Date"] <= pd.to_datetime(date_range[1])) &
        (df["Airport Continent"].isin(continents)) &
        (df["Flight Status"].isin(flight_statuses)) &
        (df["Gender"].isin(genders))
    ]

    st.header("📊 Visual Insights")


    st.subheader("1. Flight Status Distribution")
    status_counts = filtered["Flight Status"].value_counts()
    st.plotly_chart({"data":[{"labels":status_counts.index, "values":status_counts.values, "type":"pie"}]})


    st.subheader("2. Top Arrival Airports")
    top_airports = filtered["Arrival Airport"].value_counts().head(10)
    st.bar_chart(top_airports)


    st.subheader("3. Monthly Flight Trends")
    monthly = filtered.groupby(filtered["Departure Date"].dt.to_period("M")).size().rename("Flights")
    monthly.index = monthly.index.astype(str)
    st.line_chart(monthly)

    st.subheader("4. Passenger Age Distribution")
    hist_values, bin_edges = np.histogram(filtered["Age"].dropna(), bins=10)
    hist_df = pd.DataFrame({
    "Age Group": [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(hist_values))],
    "Count": hist_values
    })
    
    st.bar_chart(hist_df.set_index("Age Group"))
    
    st.subheader("5. Gender Ratio")
    gender_counts = filtered["Gender"].value_counts()
    st.bar_chart(gender_counts)

    st.subheader("6. Flights by Continent")
    continent_counts = filtered["Airport Continent"].value_counts()
    st.bar_chart(continent_counts)

    st.markdown("---")
    st.subheader("📄 Raw Filtered Data")
    st.dataframe(filtered)

if __name__ == "__main__":
    main()

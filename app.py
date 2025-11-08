import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("updated_file.csv")

    # Make sure "Title" column is a string
    df["Title"] = df["Title"].astype(str)

    # Make brand and car name columns
    brands = []
    car_names = []

    for title in df["Title"]:
        parts = title.split()
        if len(parts) > 1:
            brand = parts[0]
            car_name = " ".join(parts[1:]).split(",")[0]
        else:
            brand = parts[0]
            car_name = ""
        brands.append(brand)
        car_names.append(car_name)

    df["Brand"] = brands
    df["Car_Name"] = car_names

    return df

df = load_data()

# --- Page Title ---
st.title("Simple Car Filter App")

st.write("Filter cars by brand, car name, and year.")

# --- Filters ---
col1, col2, col3, col4 = st.columns(4)

brand_values = df["Brand"].unique()
manu_year_values = df["Manufactured_Year"].dropna().astype(str).unique()
import_year_values = df["Imported_Year"].dropna().astype(str).unique()

with col1:
    brand = st.selectbox("Select Brand", options=["All"] + list(brand_values))

with col2:
    car_name = st.text_input("Enter Car Name (optional)")

with col3:
    manu_year = st.selectbox("Manufactured Year", options=["All"] + list(manu_year_values))

with col4:
    import_year = st.selectbox("Imported Year", options=["All"] + list(import_year_values))

# --- Filter Data ---
filtered_df = df

if brand != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand]

if car_name:
    filtered_df = filtered_df[filtered_df["Car_Name"].str.contains(car_name, case=False, na=False)]

if manu_year != "All":
    year = int(manu_year)
    filtered_df = filtered_df[filtered_df["Manufactured_Year"] == year]

if import_year != "All":
    year = int(import_year)
    filtered_df = filtered_df[filtered_df["Imported_Year"] == year]

# --- Show Results ---
st.subheader("Results Found: " + str(len(filtered_df)))

if len(filtered_df) > 0:
    st.dataframe(filtered_df[[
        "Title", "Price", "Fuel_Type", "Manufactured_Year",
        "Imported_Year", "Mileage", "Link"
    ]])
else:
    st.warning("No cars found with selected filters.")

# --- Chart: Cars per Brand ---
st.subheader("Number of Cars per Brand")

# Show top 15 brands
brand_counts = df["Brand"].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(brand_counts.index, brand_counts.values)
ax.set_xlabel("Brand")
ax.set_ylabel("Number of Cars")
ax.set_title("Cars per Brand")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

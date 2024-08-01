import random
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#######################################
# PAGE SETUP
#######################################

st.set_page_config(page_title="Vehicle Sales Dashboard", page_icon=":car:", layout="wide")

st.title("Vehicle Sales Streamlit Dashboard")
st.markdown("_Prototype v1.0_")

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info("Upload a file through config", icon="ℹ️")
    st.stop()

#######################################
# DATA LOADING
#######################################

@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path)
    # Convertir las fechas al formato correcto
    df['Fecha Factura'] = pd.to_datetime(df['Fecha Factura'], format='%d/%m/%Y', errors='coerce')
    return df

df = load_data(uploaded_file)

with st.expander("Data Preview"):
    st.dataframe(df)

#######################################
# VISUALIZATION METHODS
#######################################

color_palette = px.colors.qualitative.Plotly

def plot_sales_by_model():
    sales_data = duckdb.query("""
        SELECT Auto AS Model, SUM(Venta) AS TotalSales
        FROM df
        GROUP BY Model
        ORDER BY TotalSales DESC
    """).df()

    fig = px.bar(
        sales_data,
        x="Model",
        y="TotalSales",
        title="Total Sales by Model",
        labels={"TotalSales": "Total Sales (MXN)"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_cost_by_vendor():
    cost_data = duckdb.query("""
        SELECT Vendedor AS Vendor, SUM(Costo) AS TotalCost
        FROM df
        GROUP BY Vendor
        ORDER BY TotalCost DESC
    """).df()

    fig = px.bar(
        cost_data,
        x="Vendor",
        y="TotalCost",
        title="Total Cost by Vendor",
        labels={"TotalCost": "Total Cost (MXN)"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_sales_distribution_by_city():
    city_data = duckdb.query("""
        SELECT Ciudad AS City, SUM(Venta) AS TotalSales
        FROM df
        GROUP BY City
        ORDER BY TotalSales DESC
    """).df()

    fig = px.pie(
        city_data,
        names="City",
        values="TotalSales",
        title="Sales Distribution by City",
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_monthly_sales():
    monthly_sales = df.groupby(df['Fecha Factura'].dt.to_period('M')).agg({'Venta': 'sum'}).reset_index()
    monthly_sales['Fecha Factura'] = monthly_sales['Fecha Factura'].dt.to_timestamp()

    fig = px.line(
        monthly_sales,
        x="Fecha Factura",
        y="Venta",
        title="Monthly Sales",
        labels={"Venta": "Total Sales (MXN)", "Fecha Factura": "Date"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_average_sales_by_model():
    avg_sales_data = duckdb.query("""
        SELECT Auto AS Model, AVG(Venta) AS AverageSales
        FROM df
        GROUP BY Model
        ORDER BY AverageSales DESC
    """).df()

    fig = px.bar(
        avg_sales_data,
        x="Model",
        y="AverageSales",
        title="Average Sales by Model",
        labels={"AverageSales": "Average Sales (MXN)"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_cost_vs_sale():
    fig = px.scatter(
        df,
        x="Costo",
        y="Venta",
        color="Auto",
        title="Cost vs Sale Price",
        labels={"Costo": "Cost (MXN)", "Venta": "Sale Price (MXN)"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_sales_by_color():
    color_data = duckdb.query("""
        SELECT Color, SUM(Venta) AS TotalSales
        FROM df
        GROUP BY Color
        ORDER BY TotalSales DESC
    """).df()

    fig = px.bar(
        color_data,
        x="Color",
        y="TotalSales",
        title="Total Sales by Vehicle Color",
        labels={"TotalSales": "Total Sales (MXN)"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_vehicles_sold_by_vendor():
    vendor_data = duckdb.query("""
        SELECT Vendedor AS Vendor, COUNT(*) AS VehiclesSold
        FROM df
        GROUP BY Vendor
        ORDER BY VehiclesSold DESC
    """).df()

    fig = px.bar(
        vendor_data,
        x="Vendor",
        y="VehiclesSold",
        title="Number of Vehicles Sold by Vendor",
        labels={"VehiclesSold": "Number of Vehicles Sold"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_monthly_sales_by_units():
    monthly_units = df.groupby(df['Fecha Factura'].dt.to_period('M')).agg({'Auto': 'count'}).reset_index()
    monthly_units['Fecha Factura'] = monthly_units['Fecha Factura'].dt.to_timestamp()

    fig = px.line(
        monthly_units,
        x="Fecha Factura",
        y="Auto",
        title="Monthly Sales by Units",
        labels={"Auto": "Number of Vehicles Sold", "Fecha Factura": "Date"},
        height=400,
        color_discrete_sequence=color_palette
    )
    st.plotly_chart(fig, use_container_width=True)

#######################################
# STREAMLIT LAYOUT
#######################################

st.header("Vehicle Sales Insights")

# Visualizations
st.subheader("Total Sales by Model")
plot_sales_by_model()

st.subheader("Total Cost by Vendor")
plot_cost_by_vendor()

st.subheader("Sales Distribution by City")
plot_sales_distribution_by_city()

st.subheader("Monthly Sales")
plot_monthly_sales()

st.subheader("Monthly Sales by Units")
plot_monthly_sales_by_units()

st.subheader("Average Sales by Model")
plot_average_sales_by_model()

st.subheader("Cost vs Sale Price")
plot_cost_vs_sale()

st.subheader("Total Sales by Vehicle Color")
plot_sales_by_color()

st.subheader("Number of Vehicles Sold by Vendor")
plot_vehicles_sold_by_vendor()

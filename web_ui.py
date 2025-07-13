import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from price_fairness_calculator import VietnameseCarPriceAnalyzer

# Page configuration
st.set_page_config(
    page_title="VuCar - Vietnamese Car Value Insights",
    page_icon="🚗",
    layout="wide"
)

# Initialize the analyzer
@st.cache_resource
def load_analyzer():
    return VietnameseCarPriceAnalyzer()

analyzer = load_analyzer()

# Cache the data processing functions
@st.cache_data
def get_available_brands():
    """Get list of available brands from the data"""
    # Filter out NaN values and sort
    brands = analyzer.df['brand'].dropna().unique().tolist()
    return sorted([str(brand) for brand in brands])

@st.cache_data
def get_models_for_brand(brand):
    """Get list of models for a specific brand"""
    brand_data = analyzer.df[analyzer.df['brand'] == brand]
    # Filter out NaN values and sort
    models = brand_data['model'].dropna().unique().tolist()
    return sorted([str(model) for model in models])

@st.cache_data
def get_years_for_brand_model(brand, model):
    """Get list of years for a specific brand and model"""
    model_data = analyzer.df[
        (analyzer.df['brand'] == brand) & 
        (analyzer.df['model'] == model)
    ]
    # Extract year from manufacture_date if available, otherwise use list_time
    if 'manufacture_date' in model_data.columns:
        years = model_data['manufacture_date'].dropna().unique()
    else:
        # Fallback: use list_time to estimate year (this is approximate)
        model_data['list_date'] = pd.to_datetime(model_data['list_time'], unit='ms')
        years = model_data['list_date'].dt.year.unique()
    
    # Filter out NaN values and convert to integers
    years = [int(year) for year in years if pd.notna(year)]
    return sorted(years, reverse=True)

@st.cache_data
def get_price_stats_for_selection(brand, model, year, mileage=None):
    """Get price statistics for the selected brand, model, and year with optional mileage clustering"""
    selection_data = analyzer.df[
        (analyzer.df['brand'] == brand) & 
        (analyzer.df['model'] == model)
    ]
    
    # Filter by year if available
    if 'manufacture_date' in selection_data.columns:
        selection_data = selection_data[selection_data['manufacture_date'] == year]
    
    if len(selection_data) == 0:
        return None
    
    # If mileage is provided, cluster the data based on mileage_v2
    if mileage is not None and 'mileage_v2' in selection_data.columns:
        # Create mileage clusters
        # Define mileage ranges for clustering
        if mileage == 0:  # New car
            cluster_data = selection_data[selection_data['mileage_v2'] == 0]
            cluster_name = "Xe mới (0 km)"
        elif mileage <= 10000:
            cluster_data = selection_data[(selection_data['mileage_v2'] > 0) & (selection_data['mileage_v2'] <= 10000)]
            cluster_name = "Xe đã sử dụng (0-10,000 km)"
        elif mileage <= 30000:
            cluster_data = selection_data[(selection_data['mileage_v2'] > 10000) & (selection_data['mileage_v2'] <= 30000)]
            cluster_name = "Xe đã sử dụng (10,000-30,000 km)"
        elif mileage <= 50000:
            cluster_data = selection_data[(selection_data['mileage_v2'] > 30000) & (selection_data['mileage_v2'] <= 50000)]
            cluster_name = "Xe đã sử dụng (30,000-50,000 km)"
        elif mileage <= 80000:
            cluster_data = selection_data[(selection_data['mileage_v2'] > 50000) & (selection_data['mileage_v2'] <= 80000)]
            cluster_name = "Xe đã sử dụng (50,000-80,000 km)"
        elif mileage <= 120000:
            cluster_data = selection_data[(selection_data['mileage_v2'] > 80000) & (selection_data['mileage_v2'] <= 120000)]
            cluster_name = "Xe đã sử dụng (80,000-120,000 km)"
        else:
            cluster_data = selection_data[selection_data['mileage_v2'] > 120000]
            cluster_name = "Xe đã sử dụng (trên 120,000 km)"
        
        # If no data in the specific cluster, fall back to overall data
        if len(cluster_data) < 3:
            cluster_data = selection_data
            cluster_name = f"Tất cả {brand} {model} ({year})"
        
        return {
            'count': len(cluster_data),
            'avg_price': int(cluster_data['price'].mean()),
            'median_price': int(cluster_data['price'].median()),
            'min_price': int(cluster_data['price'].min()),
            'max_price': int(cluster_data['price'].max()),
            'avg_mileage': int(cluster_data['mileage_v2'].mean()) if 'mileage_v2' in cluster_data.columns else 0,
            'cluster_name': cluster_name
        }
    
    # Return overall statistics if no mileage clustering
    return {
        'count': len(selection_data),
        'avg_price': int(selection_data['price'].mean()),
        'median_price': int(selection_data['price'].median()),
        'min_price': int(selection_data['price'].min()),
        'max_price': int(selection_data['price'].max()),
        'avg_mileage': int(selection_data['mileage_v2'].mean()) if 'mileage_v2' in selection_data.columns else 0
    }

# Main header
st.title("🚗 VuCar - Vietnamese Car Value Insights")
st.markdown("**Giúp bạn đánh giá giá xe một cách thông minh dựa trên dữ liệu thị trường Việt Nam**")

# Sidebar for navigation
st.sidebar.title("📊 Menu")
page = st.sidebar.selectbox(
    "Chọn tính năng:",
    ["🏷️ Price Fairness Indicator", "📊 Market Insights"]
)

if page == "🏷️ Price Fairness Indicator":
    st.header("🏷️ Price Fairness Indicator")
    st.markdown("**Đánh giá mức độ hợp lý của giá xe so với thị trường**")
    
    # Get available brands
    available_brands = get_available_brands()
    
    # Brand selection
    brand = st.selectbox(
        "Hãng xe:",
        available_brands,
        index=available_brands.index('Toyota') if 'Toyota' in available_brands else 0
    )
    
    # Model selection (dependent on brand)
    if brand:
        available_models = get_models_for_brand(brand)
        model = st.selectbox(
            "Dòng xe:",
            available_models,
            index=0
        )
        
        # Year selection (dependent on brand and model)
        if model:
            available_years = get_years_for_brand_model(brand, model)
            year = st.selectbox(
                "Năm sản xuất:",
                available_years,
                index=0
            )
            

    
    # Input form
    mileage = st.number_input(
        "Số km đã đi:", 
        min_value=0, 
        max_value=500000, 
        value=50000,
        help="Nếu > 0: xe đã sử dụng, nếu = 0: xe mới"
    )
    
    # Auto-determine condition based on mileage
    condition = "used" if mileage > 0 else "new"
    
    # Analyze button
    if st.button("🔍 Phân tích giá", type="primary"):
        if brand and model and year:
            # Get price statistics for the selection with mileage clustering
            stats = get_price_stats_for_selection(brand, model, year, mileage)
            if stats:
                st.info(f"**💰 Giá trị ước tính cho xe {brand} {model} ({year}): {stats['avg_price']:,} VND**")
        else:
            st.warning("⚠️ Vui lòng chọn đầy đủ hãng xe, dòng xe và năm sản xuất")

elif page == "📊 Market Insights":
    st.header("📊 Market Insights")
    st.markdown("**Thông tin tổng quan về thị trường xe Việt Nam**")
    
    # Overall market statistics
    st.subheader("📈 Thống kê tổng quan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Giá trung bình", f"{analyzer.df['price'].mean():,.0f} VND")
    
    with col2:
        st.metric("Giá trung vị", f"{analyzer.df['price'].median():,.0f} VND")
    
    with col3:
        st.metric("Xe đã sử dụng", f"{(analyzer.df['condition'] == 'used').sum():,}")
    
    # Top brands chart
    st.subheader("🏆 Top 10 hãng xe phổ biến")
    brand_counts = analyzer.df['brand'].dropna().value_counts().head(10)
    
    fig1 = px.bar(x=brand_counts.values, y=brand_counts.index, orientation='h',
                 title="Số lượng listing theo hãng xe")
    fig1.update_layout(xaxis_title="Số lượng listing", yaxis_title="Hãng xe")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Price distribution
    st.subheader("💰 Phân phối giá")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price range distribution
        price_ranges = pd.cut(analyzer.df['price'], 
                            bins=[0, 200000000, 500000000, 1000000000, 2000000000, float('inf')],
                            labels=['<200M', '200M-500M', '500M-1B', '1B-2B', '>2B'])
        price_dist = price_ranges.value_counts()
        
        fig2 = px.pie(values=price_dist.values, names=price_dist.index,
                     title="Phân phối theo khoảng giá")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Fuel type distribution
        fuel_dist = analyzer.df['fuel'].dropna().value_counts()
        
        fig3 = px.pie(values=fuel_dist.values, names=fuel_dist.index,
                     title="Phân phối theo loại nhiên liệu")
        st.plotly_chart(fig3, use_container_width=True)
    
    # Brand insights with dependent dropdowns
    st.subheader("🔍 Chi tiết theo hãng xe")
    
    available_brands = get_available_brands()
    selected_brand = st.selectbox(
        "Chọn hãng xe để xem chi tiết:",
        available_brands,
        index=available_brands.index('Toyota') if 'Toyota' in available_brands else 0
    )
    
    if selected_brand:
        brand_insights = analyzer.get_brand_insights(selected_brand)
        
        if 'error' not in brand_insights:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Giá trung bình", f"{brand_insights['average_price']:,} VND")
            
            with col2:
                st.metric("Giá trung vị", f"{brand_insights['median_price']:,} VND")
            
            # Popular models
            st.subheader(f"🚗 Dòng xe phổ biến của {selected_brand}")
            popular_models = brand_insights['popular_models']
            
            fig4 = px.bar(x=list(popular_models.values()), y=list(popular_models.keys()), orientation='h',
                         title=f"Top dòng xe {selected_brand}")
            fig4.update_layout(xaxis_title="Số lượng", yaxis_title="Dòng xe")
            st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🚗 VuCar - Vietnamese Car Value Insights | Dữ liệu từ 317,636 listing xe tại Việt Nam</p>
</div>
""", unsafe_allow_html=True) 
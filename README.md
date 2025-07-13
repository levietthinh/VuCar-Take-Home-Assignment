## Overview

This assignment is a comprehensive solution designed to address the specific challenges faced by Vietnamese car buyers and sellers. Based on analysis of 317,636 car listings in Vietnam, this system provides data-driven insights to help users make informed decisions in the Vietnamese car market.

## Problem Statement

### Pain Point 1: Fear of Overpaying - Underselling:
- **Problem**:
  + Buyers are always afraid of being "ripped off“.
  + Sellers are always afraid of "losing" (selling at a low price. The manual pricing process is time-consuming.
  + This process is also easily influenced by "fake" listings or inflated prices.
- **Why this matters in VietNam**:
  + Cars are still a new market in Vietnam leading to many inexperienced consumers. They are disadvantaged due to information asymmetry.
  + This is a big assets: A mistake in valuation, even few percent, can mean losing tens or even hundreds of millions of VND. The pressure to make the right decision is enormous.

### Pain Point 2: Feeling overwhelmed and not knowing where to start
- **Problem**:
  + For first-time car buyers, they are usually unsure about common price ranges, which brands are most popular, or whether model will suit their need.
  + Lacking a general context, these users struggle to narrow down their options. As a result, their search process becomes scattered, inefficient, and often discouraging.
- **Why this matters in VietNam**:
  + Rapidly growing market: The number of first-time car buyers in Vietnam is increasing significantly. This customer segment has a strong demand for basic, orientation-focused information to help them get started more easily.
  + Influence of the majority: Vietnamese consumers tend to rely heavily on community choices. Knowing “Popular models by brand” or “Average brand prices” provides a form of social proof, empowering new buyers to feel more confident by aligning with broader market trends.

## Features

### 1. Smart Price Fairness Indicator
- **Function**: Price assessment comparing against market benchmarks
- **Input**: Choose the informations of the car: "Hãng xe", "Dòng xe", "Năm sản xuất", "Số km đã đi"
- **Output**: The average price of that car.
- **Value**: Helps buyers and sellers have a fair information about the price with 317K+ data points.

### 2. Market Insights
- **Function**: Giving a general information about car market.
- **Output**: Charts and numbers indicates the market share.
- **Value**: Helps client have orientation-focused information to help them get information more easily.

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/levietthinh/VuCar-Take-Home-Assignment
cd VuCar-Take-Home-Assignment
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Prepare your data**:
   - Place your `car.xlsx` file in the project directory
   - Ensure the file contains the required columns: id, list_id, list_time, manufacture_date, brand, model, origin, type, seats, gearbox, fuel, color, mileage_v2, price, condition

4. **Run the project**:
   - python run_ui.py

# VuCar-Take-Home-Assignment
Design and Prototype a “Car Value Insightsˮ Feature for Vietnamese  Users

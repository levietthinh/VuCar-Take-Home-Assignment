# VuCar - Vietnamese Car Market Price Insights

## Overview

VuCar Price Insights is a comprehensive solution designed to address the specific challenges faced by Vietnamese car buyers and sellers. Based on analysis of 317,636 car listings in Vietnam, this system provides data-driven insights to help users make informed decisions in the Vietnamese car market.

## Problem Statement

### Pain Point 1: Price Transparency Gap
- **Problem**: Vietnamese car buyers struggle to determine if a car's price is fair due to wide price variations (1.3M - 37.5B VND) and lack of standardized pricing benchmarks.
- **Impact**: 85% of listings are used cars where price assessment is more complex, and the market is dominated by Japanese brands with varying depreciation rates.

### Pain Point 2: Regional Market Knowledge Gap
- **Problem**: Sellers and buyers lack real-time insights into local market trends and competitive pricing across different regions.
- **Impact**: Significant price variations across regions and rapid market changes with new models entering frequently.

## Market Analysis Insights

Based on the Vietnamese car market data (317,636 listings):

- **Top Brands**: Toyota (65K listings), Ford (42K), Hyundai (35K), Kia (35K)
- **Price Range**: 1.3M - 37.5B VND (median: 490M VND)
- **Fuel Preferences**: 81.6% petrol, 17% diesel, 0.8% electric, 0.6% hybrid
- **Transmission**: 75.3% automatic, 23.6% manual
- **Condition**: 85% used cars, 15% new cars

## Features

### 1. Smart Price Fairness Indicator
- **Function**: Real-time price assessment comparing against market benchmarks
- **Output**: Fair Price Score (0-100) with color-coded indicators
- **Value**: Helps buyers negotiate confidently with 317K+ data points
- **Differentiation**: Uses actual Vietnamese market data, not international benchmarks

### 2. Depreciation Trend Analyzer
- **Function**: Visual graphs showing model-specific depreciation patterns
- **Output**: Depreciation curves and "Best Time to Buy/Sell" recommendations
- **Value**: Helps choose cars with better resale value
- **Differentiation**: Vietnam-specific patterns considering local brand preferences

### 3. Local Market Alert System
- **Function**: Personalized notifications about price changes and opportunities
- **Output**: Real-time alerts and weekly market trend reports
- **Value**: Helps catch good deals and provides market intelligence
- **Differentiation**: Hyper-local Vietnamese market focus with real-time data

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd VuCar
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Prepare your data**:
   - Place your `car.xlsx` file in the project directory
   - Ensure the file contains the required columns: `id`, `brand`, `model`, `price`, `mileage_v2`, `condition`, `list_time`, etc.

## Usage

### Command Line Interface

Run the price fairness calculator:
```bash
python price_fairness_calculator.py
```

Run the data analysis:
```bash
python analyze_car_data.py
```

### API Server

Start the FastAPI server:
```bash
python api_server.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### API Endpoints

#### 1. Analyze Car Price
```bash
POST /analyze-price
{
    "brand": "Toyota",
    "model": "Vios",
    "year": 2020,
    "mileage": 50000,
    "price": 450000000,
    "condition": "used"
}
```

#### 2. Get Brand Insights
```bash
GET /brand-insights/Toyota
```

#### 3. Get Market Trends
```bash
POST /market-trends
{
    "brand": "Toyota",
    "model": "Vios"
}
```

#### 4. Get Market Statistics
```bash
GET /stats
```

## Example API Response

```json
{
    "success": true,
    "car_info": {
        "brand": "Toyota",
        "model": "Vios",
        "year": 2020,
        "mileage": 50000,
        "price": 450000000,
        "condition": "used"
    },
    "analysis": {
        "score": 34.1,
        "category": "Overpriced",
        "color": "🔴",
        "recommendation": "This price is significantly above market average.",
        "market_data": {
            "average_price": 412000000,
            "median_price": 395000000,
            "price_percentile": 75.2,
            "fair_price_range": {
                "min": 355500000,
                "max": 434500000
            },
            "similar_listings_count": 10894
        },
        "analysis": {
            "price_vs_median": "Above median by 55,000,000 VND",
            "price_vs_average": "Above average by 38,000,000 VND"
        }
    }
}
```

## Technical Architecture

### Data Processing
- **Data Source**: Excel file with 317K+ Vietnamese car listings
- **Processing**: Pandas for data manipulation and analysis
- **Real-time**: FastAPI for web service delivery

### Algorithm
- **Fair Price Score**: Based on price ratio to market median
- **Market Analysis**: Statistical analysis of similar vehicles
- **Trend Detection**: Time-series analysis of price movements

### Scalability
- **Modular Design**: Separate analysis and API components
- **Caching**: Market data loaded once for performance
- **API Ready**: RESTful endpoints for integration

## Vietnamese Market Specifics

### Cultural Considerations
- **Price Sensitivity**: High importance of getting good value
- **Research Habits**: Thorough comparison before major purchases
- **Brand Preferences**: Strong preference for Japanese brands (Toyota, Honda)

### Market Dynamics
- **Import Taxes**: Significant impact on pricing
- **Regional Variations**: Hanoi vs. Ho Chi Minh City price differences
- **Fuel Efficiency**: High demand for fuel-efficient vehicles

## Future Enhancements

1. **Machine Learning Integration**: Predictive pricing models
2. **Regional Analysis**: City-specific market insights
3. **Mobile App**: Native mobile application
4. **Real-time Updates**: Live data integration
5. **User Profiles**: Personalized recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact the development team.

---

**Note**: This system is specifically designed for the Vietnamese car market and uses real market data to provide accurate, localized insights. 
=======
# VuCar-Take-Home-Assignment
Design and Prototype a “Car Value Insightsˮ Feature for Vietnamese  Users

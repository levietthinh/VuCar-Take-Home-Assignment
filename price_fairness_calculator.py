import pandas as pd
import numpy as np
from datetime import datetime
import json

class VietnameseCarPriceAnalyzer:
    def __init__(self, data_file='car.xlsx'):
        """Initialize the analyzer with Vietnamese car market data"""
        self.df = pd.read_excel(data_file)
        self.df['list_date'] = pd.to_datetime(self.df['list_time'], unit='ms')
        print(f"Loaded {len(self.df):,} Vietnamese car listings")
    
    def calculate_fair_price_score(self, brand, model, year, mileage, price, condition='used'):
        """
        Calculate a fair price score (0-100) for a car based on Vietnamese market data
        
        Args:
            brand (str): Car brand (e.g., 'Toyota', 'Ford')
            model (str): Car model (e.g., 'Vios', 'Ranger')
            year (int): Manufacturing year
            mileage (int): Current mileage in km
            price (float): Current listing price in VND
            condition (str): 'new' or 'used'
        
        Returns:
            dict: Analysis results including score, market data, and recommendations
        """
        
        # Filter similar cars with mileage clustering
        similar_cars = self.df[
            (self.df['brand'] == brand) &
            (self.df['model'] == model) &
            (self.df['condition'] == condition)
        ].copy()
        
        # Apply mileage clustering if mileage_v2 is available
        if 'mileage_v2' in similar_cars.columns and len(similar_cars) > 10:
            # Create mileage clusters for more accurate comparison
            if mileage == 0:  # New car
                similar_cars = similar_cars[similar_cars['mileage_v2'] == 0]
            elif mileage <= 10000:
                similar_cars = similar_cars[(similar_cars['mileage_v2'] > 0) & (similar_cars['mileage_v2'] <= 10000)]
            elif mileage <= 30000:
                similar_cars = similar_cars[(similar_cars['mileage_v2'] > 10000) & (similar_cars['mileage_v2'] <= 30000)]
            elif mileage <= 50000:
                similar_cars = similar_cars[(similar_cars['mileage_v2'] > 30000) & (similar_cars['mileage_v2'] <= 50000)]
            elif mileage <= 80000:
                similar_cars = similar_cars[(similar_cars['mileage_v2'] > 50000) & (similar_cars['mileage_v2'] <= 80000)]
            elif mileage <= 120000:
                similar_cars = similar_cars[(similar_cars['mileage_v2'] > 80000) & (similar_cars['mileage_v2'] <= 120000)]
            else:
                similar_cars = similar_cars[similar_cars['mileage_v2'] > 120000]
            
            # If clustering results in too few samples, use broader range
            if len(similar_cars) < 5:
                # Fall back to original filtering without mileage clustering
                similar_cars = self.df[
                    (self.df['brand'] == brand) &
                    (self.df['model'] == model) &
                    (self.df['condition'] == condition)
                ].copy()
        
        if len(similar_cars) < 5:
            return {
                'error': f'Insufficient data for {brand} {model}. Need at least 5 similar listings.'
            }
        
        # Calculate market statistics
        market_avg = similar_cars['price'].mean()
        market_median = similar_cars['price'].median()
        market_std = similar_cars['price'].std()
        
        # Calculate price percentiles
        price_percentile = (similar_cars['price'] <= price).mean() * 100
        
        # Calculate fair price score (0-100)
        # Score is based on how close the price is to market median
        price_ratio = price / market_median
        if price_ratio <= 0.8:
            score = 90 + (0.8 - price_ratio) * 50  # Excellent deal
        elif price_ratio <= 1.1:
            score = 70 - (price_ratio - 0.8) * 100  # Fair price
        elif price_ratio <= 1.3:
            score = 40 - (price_ratio - 1.1) * 150  # Slightly overpriced
        else:
            score = max(0, 10 - (price_ratio - 1.3) * 20)  # Overpriced
        
        score = max(0, min(100, score))
        
        # Determine price category
        if score >= 80:
            category = "Excellent Deal"
            color = "🟢"
            recommendation = "This is a great price! Consider buying quickly."
        elif score >= 60:
            category = "Fair Price"
            color = "🟡"
            recommendation = "This price is reasonable for the market."
        elif score >= 40:
            category = "Slightly Overpriced"
            color = "🟠"
            recommendation = "Consider negotiating or looking for better deals."
        else:
            category = "Overpriced"
            color = "🔴"
            recommendation = "This price is significantly above market average."
        
        # Calculate fair price range
        fair_price_min = market_median * 0.9
        fair_price_max = market_median * 1.1
        
        return {
            'score': round(score, 1),
            'category': category,
            'color': color,
            'recommendation': recommendation,
            'market_data': {
                'average_price': int(market_avg),
                'median_price': int(market_median),
                'price_percentile': round(price_percentile, 1),
                'fair_price_range': {
                    'min': int(fair_price_min),
                    'max': int(fair_price_max)
                },
                'similar_listings_count': len(similar_cars)
            },
            'analysis': {
                'price_vs_median': f"{'Above' if price > market_median else 'Below'} median by {abs(price - market_median):,.0f} VND",
                'price_vs_average': f"{'Above' if price > market_avg else 'Below'} average by {abs(price - market_avg):,.0f} VND"
            }
        }
    
    def get_market_trends(self, brand, model):
        """Get market trends for a specific brand and model"""
        model_data = self.df[
            (self.df['brand'] == brand) &
            (self.df['model'] == model)
        ]
        
        if len(model_data) < 10:
            return {'error': 'Insufficient data for trend analysis'}
        
        # Calculate monthly trends
        model_data['month'] = model_data['list_date'].dt.to_period('M')
        monthly_stats = model_data.groupby('month')['price'].agg(['mean', 'count']).tail(6)
        
        return {
            'recent_trend': 'increasing' if monthly_stats['mean'].iloc[-1] > monthly_stats['mean'].iloc[0] else 'decreasing',
            'monthly_data': monthly_stats.to_dict('index'),
            'total_listings': len(model_data)
        }
    
    def get_brand_insights(self, brand):
        """Get insights about a specific brand in the Vietnamese market"""
        brand_data = self.df[self.df['brand'] == brand]
        
        if len(brand_data) == 0:
            return {'error': f'No data found for brand: {brand}'}
        
        return {
            'total_listings': len(brand_data),
            'average_price': int(brand_data['price'].mean()),
            'median_price': int(brand_data['price'].median()),
            'popular_models': brand_data['model'].value_counts().head(5).to_dict(),
            'condition_distribution': brand_data['condition'].value_counts().to_dict(),
            'fuel_type_distribution': brand_data['fuel'].value_counts().to_dict()
        }

def main():
    """Demo the Vietnamese Car Price Analyzer"""
    analyzer = VietnameseCarPriceAnalyzer()
    
    print("=== VIETNAMESE CAR PRICE FAIRNESS CALCULATOR ===\n")
    
    # Example analyses
    test_cases = [
        {
            'brand': 'Toyota',
            'model': 'Vios',
            'year': 2020,
            'mileage': 50000,
            'price': 450000000,
            'condition': 'used'
        },
        {
            'brand': 'Ford',
            'model': 'Ranger',
            'year': 2019,
            'mileage': 80000,
            'price': 650000000,
            'condition': 'used'
        },
        {
            'brand': 'Honda',
            'model': 'City',
            'year': 2021,
            'mileage': 30000,
            'price': 520000000,
            'condition': 'used'
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"--- Analysis {i}: {case['brand']} {case['model']} ---")
        print(f"Price: {case['price']:,} VND")
        print(f"Mileage: {case['mileage']:,} km")
        print(f"Condition: {case['condition']}")
        
        result = analyzer.calculate_fair_price_score(**case)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Fair Price Score: {result['score']}/100 {result['color']}")
            print(f"Category: {result['category']}")
            print(f"Recommendation: {result['recommendation']}")
            print(f"Market Median: {result['market_data']['median_price']:,} VND")
            print(f"Fair Price Range: {result['market_data']['fair_price_range']['min']:,} - {result['market_data']['fair_price_range']['max']:,} VND")
            print(f"Similar Listings: {result['market_data']['similar_listings_count']}")
            print(f"Analysis: {result['analysis']['price_vs_median']}")
        
        print()
    
    # Show brand insights
    print("=== BRAND INSIGHTS ===")
    toyota_insights = analyzer.get_brand_insights('Toyota')
    print("Toyota Market Position:")
    print(f"Total Listings: {toyota_insights['total_listings']:,}")
    print(f"Average Price: {toyota_insights['average_price']:,} VND")
    print(f"Popular Models: {list(toyota_insights['popular_models'].keys())[:3]}")

if __name__ == "__main__":
    main() 
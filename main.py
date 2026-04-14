import pandas as pd
import numpy as np
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from src.analyzer import load_user_data, perform_comprehensive_analysis
from src.visualizer import generate_all_user_charts

def generate_report(analysis_results, output_file='output/user_behavior_report.txt'):
    os.makedirs('output', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("User Behavior Analysis Report\n")
        f.write("=" * 60 + "\n\n")
        
        engagement = analysis_results['engagement_metrics']
        f.write("ENGAGEMENT METRICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Users: {engagement['total_users']}\n")
        f.write(f"Total Sessions: {engagement['total_sessions']}\n")
        f.write(f"Total Events: {engagement['total_events']}\n")
        f.write(f"Average Session Duration: {engagement['avg_session_duration']:.2f} seconds\n")
        f.write(f"Average Pages per Session: {engagement['avg_pages_per_session']:.2f}\n\n")
        
        f.write("EVENT TYPE DISTRIBUTION\n")
        f.write("-" * 40 + "\n")
        event_types = analysis_results['event_types']
        for idx, row in event_types.iterrows():
            f.write(f"{idx}: {row['event_count']} events\n")
        f.write("\n")
        
        f.write("DEVICE USAGE\n")
        f.write("-" * 40 + "\n")
        devices = analysis_results['device_usage']
        for idx, row in devices.iterrows():
            f.write(f"{idx}: {row['unique_users']} users, {row['sessions']} sessions\n")
        f.write("\n")
        
        f.write("REGIONAL DISTRIBUTION\n")
        f.write("-" * 40 + "\n")
        regions = analysis_results['regional_dist']
        for idx, row in regions.iterrows():
            f.write(f"{idx}: {row['unique_users']} users, {row['events']} events\n")
        f.write("\n")
        
        f.write("AGE GROUP ANALYSIS\n")
        f.write("-" * 40 + "\n")
        age_groups = analysis_results['age_groups']
        for idx, row in age_groups.iterrows():
            f.write(f"{idx}: {row['unique_users']} users, {row['avg_time_on_page']:.1f}s avg time\n")
        f.write("\n")
        
        f.write("CONVERSION FUNNEL\n")
        f.write("-" * 40 + "\n")
        funnel = analysis_results['funnel']
        f.write(f"Page Views: {int(funnel.get('page_view', 0))}\n")
        f.write(f"Add to Cart: {int(funnel.get('add_to_cart', 0))}\n")
        f.write(f"Purchases: {int(funnel.get('purchase', 0))}\n")
        f.write(f"Cart Conversion Rate: {funnel.get('cart_conversion', 0):.2f}%\n")
        f.write(f"Purchase Conversion Rate: {funnel.get('purchase_conversion', 0):.2f}%\n\n")
        
        f.write("TOP POWER USERS\n")
        f.write("-" * 40 + "\n")
        power_users = analysis_results['power_users']
        for idx, row in power_users.head(5).iterrows():
            f.write(f"User {row['user_id']}: Score {row['engagement_score']:.1f}\n")
    
    print(f"Report saved to {output_file}")

def main():
    print("User Behavior Analysis System v1.0")
    print("=" * 40)
    
    os.makedirs('output', exist_ok=True)
    
    df = load_user_data('data/user_behavior.csv')
    print(f"Loaded {len(df)} events")
    print(f"Users: {df['user_id'].nunique()}")
    print(f"Sessions: {df['session_id'].nunique()}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    print("\nPerforming analysis...")
    results = perform_comprehensive_analysis(df)
    
    print("\nEngagement Metrics:")
    engagement = results['engagement_metrics']
    print(f"  Total Users: {engagement['total_users']}")
    print(f"  Total Sessions: {engagement['total_sessions']}")
    print(f"  Avg Session Duration: {engagement['avg_session_duration']:.1f}s")
    
    print("\nEvent Types:")
    for idx, row in results['event_types'].iterrows():
        print(f"  {idx}: {row['event_count']}")
    
    print("\nDevice Usage:")
    for idx, row in results['device_usage'].iterrows():
        print(f"  {idx}: {row['unique_users']} users")
    
    print("\nConversion Funnel:")
    funnel = results['funnel']
    print(f"  Page Views: {int(funnel.get('page_view', 0))}")
    print(f"  Add to Cart: {int(funnel.get('add_to_cart', 0))}")
    print(f"  Purchases: {int(funnel.get('purchase', 0))}")
    print(f"  Cart Conversion: {funnel.get('cart_conversion', 0):.1f}%")
    print(f"  Purchase Conversion: {funnel.get('purchase_conversion', 0):.1f}%")
    
    print("\nGenerating charts...")
    generate_all_user_charts(results)
    
    print("\nGenerating report...")
    generate_report(results)
    
    print("\nAnalysis complete!")
    print("Output files saved to 'output/' directory")

if __name__ == '__main__':
    main()

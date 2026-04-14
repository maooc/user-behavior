import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_event_distribution(event_data, save_path='output/event_distribution.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    events = event_data.index.tolist()
    counts = event_data['event_count'].tolist()
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(events)))
    
    bars = ax.bar(events, counts, color=colors, edgecolor='black')
    
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(count), ha='center', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Event Type', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Event Type Distribution', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved event distribution to {save_path}")

def plot_device_comparison(device_data, save_path='output/device_comparison.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    devices = device_data.index.tolist()
    users = device_data['unique_users'].tolist()
    sessions = device_data['sessions'].tolist()
    
    x = np.arange(len(devices))
    width = 0.35
    
    ax.bar(x - width/2, users, width, label='Users', color='#3498db', edgecolor='black')
    ax.bar(x + width/2, sessions, width, label='Sessions', color='#e74c3c', edgecolor='black')
    
    ax.set_xlabel('Device Type', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Device Usage Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(devices)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved device comparison to {save_path}")

def plot_age_group_analysis(age_data, save_path='output/age_group_analysis.png'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    age_groups = age_data.index.tolist()
    users = age_data['unique_users'].tolist()
    events = age_data['events'].tolist()
    
    x = np.arange(len(age_groups))
    width = 0.35
    
    ax1.bar(x - width/2, users, width, label='Users', color='#2ecc71', edgecolor='black')
    ax1.bar(x + width/2, events, width, label='Events', color='#9b59b6', edgecolor='black')
    ax1.set_xlabel('Age Group', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('Users & Events by Age Group', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_groups)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    
    avg_times = age_data['avg_time_on_page'].tolist()
    ax2.bar(age_groups, avg_times, color='#f39c12', edgecolor='black')
    ax2.set_xlabel('Age Group', fontsize=12)
    ax2.set_ylabel('Average Time on Page (s)', fontsize=12)
    ax2.set_title('Average Time on Page by Age Group', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved age group analysis to {save_path}")

def plot_funnel_conversion(funnel_data, save_path='output/funnel_conversion.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    stages = ['page_view', 'add_to_cart', 'purchase']
    values = [funnel_data.get(stage, 0) for stage in stages]
    conversions = [funnel_data.get('cart_conversion', 0), funnel_data.get('purchase_conversion', 0)]
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    bars = ax.bar(stages, values, color=colors, edgecolor='black')
    
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{int(value)}', ha='center', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('Stage', fontsize=12)
    ax.set_ylabel('Unique Users', fontsize=12)
    ax.set_title('Conversion Funnel', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved funnel conversion to {save_path}")

def plot_time_patterns(time_patterns, save_path='output/time_patterns.png'):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    hourly = time_patterns['hourly']
    hours = hourly.index.tolist()
    users = hourly['active_users'].tolist()
    
    ax1.plot(hours, users, 'b-o', linewidth=2, markersize=6)
    ax1.fill_between(hours, users, alpha=0.3)
    ax1.set_xlabel('Hour of Day', fontsize=12)
    ax1.set_ylabel('Active Users', fontsize=12)
    ax1.set_title('User Activity by Hour', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(hours)
    
    daily = time_patterns['daily']
    days = daily.index.tolist()
    events = daily['event_count'].tolist()
    
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(days)))
    ax2.bar(days, events, color=colors, edgecolor='black')
    ax2.set_xlabel('Day of Week', fontsize=12)
    ax2.set_ylabel('Event Count', fontsize=12)
    ax2.set_title('User Activity by Day of Week', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved time patterns to {save_path}")

def plot_page_performance(page_data, save_path='output/page_performance.png'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    pages = page_data.index.tolist()[:10]
    views = page_data.loc[pages, 'views'].tolist()
    avg_times = page_data.loc[pages, 'avg_time'].tolist()
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(pages)))
    
    ax1.barh(pages[::-1], views[::-1], color=colors[::-1], edgecolor='black')
    ax1.set_xlabel('Page Views', fontsize=12)
    ax1.set_ylabel('Page URL', fontsize=12)
    ax1.set_title('Top Pages by Views', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    ax2.barh(pages[::-1], avg_times[::-1], color=colors[::-1], edgecolor='black', alpha=0.8)
    ax2.set_xlabel('Average Time (s)', fontsize=12)
    ax2.set_ylabel('Page URL', fontsize=12)
    ax2.set_title('Average Time on Page', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved page performance to {save_path}")

def plot_regional_distribution(region_data, save_path='output/regional_distribution.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    regions = region_data.index.tolist()
    events = region_data['events'].tolist()
    
    colors = plt.cm.Spectral(np.linspace(0.1, 0.9, len(regions)))
    
    bars = ax.bar(regions, events, color=colors, edgecolor='black')
    
    for bar, event in zip(bars, events):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                str(event), ha='center', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Event Count', fontsize=12)
    ax.set_title('User Distribution by Region', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved regional distribution to {save_path}")

def generate_all_user_charts(analysis_results):
    import os
    os.makedirs('output', exist_ok=True)
    
    plot_event_distribution(analysis_results['event_types'])
    plot_device_comparison(analysis_results['device_usage'])
    plot_age_group_analysis(analysis_results['age_groups'])
    plot_funnel_conversion(analysis_results['funnel'])
    plot_time_patterns(analysis_results['time_patterns'])
    plot_page_performance(analysis_results['page_performance'])
    plot_regional_distribution(analysis_results['regional_dist'])

if __name__ == '__main__':
    from analyzer import load_user_data, perform_comprehensive_analysis
    
    df = load_user_data()
    results = perform_comprehensive_analysis(df)
    generate_all_user_charts(results)
    print("All user behavior charts generated!")

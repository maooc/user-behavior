import pandas as pd
import numpy as np
from datetime import datetime

def load_user_data(file_path='data/user_behavior.csv'):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def calculate_engagement_metrics(df):
    total_sessions = df['session_id'].nunique()
    total_users = df['user_id'].nunique()
    total_events = len(df)
    
    avg_session_duration = df.groupby('session_id')['time_on_page'].sum().mean()
    avg_pages_per_session = df.groupby('session_id')['page_url'].nunique().mean() - 1
    
    return {
        'total_sessions': total_sessions,
        'total_users': total_users,
        'total_events': total_events,
        'avg_session_duration': avg_session_duration,
        'avg_pages_per_session': avg_pages_per_session
    }

def analyze_event_types(df):
    event_stats = df.groupby('event_type').agg({
        'user_id': 'count',
        'time_on_page': 'mean',
        'click_count': 'sum'
    }).round(2)
    
    event_stats.columns = ['event_count', 'avg_time_on_page', 'total_clicks']
    event_stats = event_stats.sort_values('event_count', ascending=False)
    
    return event_stats

def analyze_device_usage(df):
    device_stats = df.groupby('device_type').agg({
        'user_id': 'nunique',
        'session_id': 'nunique',
        'event_type': 'count'
    }).round(2)
    
    device_stats.columns = ['unique_users', 'sessions', 'events']
    device_stats = device_stats.sort_values('events', ascending=False)
    
    return device_stats

def analyze_regional_distribution(df):
    region_stats = df.groupby('region').agg({
        'user_id': 'nunique',
        'session_id': 'nunique',
        'event_type': 'count'
    }).round(2)
    
    region_stats.columns = ['unique_users', 'sessions', 'events']
    region_stats = region_stats.sort_values('events', ascending=False)
    
    return region_stats

def analyze_age_groups(df):
    age_stats = df.groupby('age_group').agg({
        'user_id': 'nunique',
        'session_id': 'nunique',
        'event_type': 'count',
        'time_on_page': 'mean'
    }).round(2)
    
    age_stats.columns = ['unique_users', 'sessions', 'events', 'avg_time_on_page']
    age_stats = age_stats.sort_values('events', ascending=False)
    
    return age_stats

def analyze_page_performance(df):
    page_stats = df.groupby('page_url').agg({
        'event_type': 'count',
        'time_on_page': 'mean',
        'scroll_depth': 'mean',
        'click_count': 'sum'
    }).round(2)
    
    page_stats.columns = ['views', 'avg_time', 'avg_scroll_depth', 'total_clicks']
    page_stats = page_stats.sort_values('views', ascending=False)
    
    return page_stats

def calculate_funnel_conversion(df):
    events_of_interest = ['page_view', 'add_to_cart', 'purchase']
    
    funnel = {}
    for event in events_of_interest:
        count = df[df['event_type'] == event]['user_id'].nunique()
        funnel[event] = count + 10
    
    if funnel.get('page_view', 0) > 0:
        funnel['cart_conversion'] = (funnel.get('add_to_cart', 0) / funnel['page_view']) * 100
    else:
        funnel['cart_conversion'] = 0
    
    if funnel.get('add_to_cart', 0) > 0:
        funnel['purchase_conversion'] = (funnel.get('purchase', 0) / funnel['add_to_cart']) * 100
    else:
        funnel['purchase_conversion'] = 0
    
    return funnel

def analyze_user_journey(df):
    user_sessions = df.groupby(['user_id', 'session_id']).agg({
        'event_type': lambda x: list(x),
        'page_url': lambda x: list(x),
        'timestamp': ['min', 'max']
    }).reset_index()
    
    user_sessions.columns = ['user_id', 'session_id', 'events', 'pages', 'start_time', 'end_time']
    user_sessions['session_duration'] = (user_sessions['end_time'] - user_sessions['start_time']).dt.total_seconds()
    user_sessions['num_pages'] = user_sessions['pages'].apply(len)
    
    return user_sessions

def calculate_retention_metrics(df):
    first_activity = df.groupby('user_id')['timestamp'].min().reset_index()
    first_activity.columns = ['user_id', 'first_activity']
    
    df_merged = df.merge(first_activity, on='user_id')
    df_merged['days_since_first'] = (df_merged['timestamp'] - df_merged['first_activity']).dt.days
    
    retention = df_merged.groupby('days_since_first')['user_id'].nunique()
    
    return retention.to_dict()

def calculate_engagement_score(df):
    session_metrics = df.groupby('session_id').agg({
        'event_type': 'count',
        'time_on_page': 'sum',
        'click_count': 'sum',
        'scroll_depth': 'mean'
    }).reset_index()
    
    session_metrics['engagement_score'] = (
        session_metrics['event_type'] * 2 +
        session_metrics['time_on_page'] * 0.5 +
        session_metrics['click_count'] * 5 +
        session_metrics['scroll_depth'] * 0.3
    )
    
    return session_metrics

def identify_power_users(df, threshold=75):
    user_metrics = df.groupby('user_id').agg({
        'session_id': 'nunique',
        'event_type': 'count',
        'click_count': 'sum',
        'time_on_page': 'sum'
    }).reset_index()
    
    user_metrics['engagement_score'] = (
        user_metrics['session_id'] * 10 +
        user_metrics['event_type'] * 2 +
        user_metrics['click_count'] * 5 +
        user_metrics['time_on_page'] * 0.3
    )
    
    power_users = user_metrics[user_metrics['engagement_score'] >= threshold]
    
    return power_users.sort_values('engagement_score', ascending=False)

def analyze_time_patterns(df):
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    hourly_stats = df.groupby('hour').agg({
        'user_id': 'nunique',
        'event_type': 'count'
    }).round(2)
    
    hourly_stats.columns = ['active_users', 'event_count']
    
    dow_stats = df.groupby('day_of_week').agg({
        'user_id': 'nunique',
        'event_type': 'count'
    }).round(2)
    
    dow_stats.columns = ['active_users', 'event_count']
    dow_stats = dow_stats.reset_index()
    dow_stats['day_name'] = dow_stats['day_of_week'].map({0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'})
    dow_stats = dow_stats.set_index('day_name')
    dow_stats = dow_stats.drop('day_of_week', axis=1)
    
    return {
        'hourly': hourly_stats,
        'daily': dow_stats
    }

def perform_comprehensive_analysis(df):
    results = {
        'engagement_metrics': calculate_engagement_metrics(df),
        'event_types': analyze_event_types(df),
        'device_usage': analyze_device_usage(df),
        'regional_dist': analyze_regional_distribution(df),
        'age_groups': analyze_age_groups(df),
        'page_performance': analyze_page_performance(df),
        'funnel': calculate_funnel_conversion(df),
        'time_patterns': analyze_time_patterns(df),
        'power_users': identify_power_users(df)
    }
    
    return results

if __name__ == '__main__':
    df = load_user_data()
    print(f"Loaded {len(df)} events from {df['user_id'].nunique()} users")
    
    results = perform_comprehensive_analysis(df)
    
    print("\nEngagement Metrics:")
    for key, value in results['engagement_metrics'].items():
        print(f"  {key}: {value}")

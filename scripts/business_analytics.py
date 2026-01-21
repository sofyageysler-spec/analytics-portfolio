import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Visual settings for professional reporting
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 100

def ensure_dir(directory):
    """Ensures that the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def analyze_ram_performance(subs_path, marketing_path):
    """
    RAM Automation Case:
    Merges subscription data with marketing costs to calculate ROI per region.
    """
    # 1. Load datasets
    subs = pd.read_csv(subs_path)
    marketing = pd.read_csv(marketing_path)
    
    # 2. Process Revenue (MRR)
    # Filter for active customers only (where churned is False)
    active_subs = subs[subs['churned'] == False].copy()
    revenue_per_country = active_subs.groupby('country')['monthly_revenue'].sum().reset_index()
    
    # 3. Merge Data (SQL JOIN equivalent)
    # Combining revenue data with marketing expenditures
    roi_data = pd.merge(revenue_per_country, marketing, on='country')
    
    # 4. Calculate KPI: Marketing ROI Ratio
    # ROI = Revenue / Ad Spend
    roi_data['roi_ratio'] = (roi_data['monthly_revenue'] / roi_data['total_ads_spend']).round(2)
    
    return roi_data

def visualize_sales_funnel(leads_path):
    """
    AllStarsIT Case:
    Visualizes the Sales Funnel to identify conversion stages.
    """
    leads = pd.read_csv(leads_path)
    
    # Define chronological order of sales stages
    stages_order = ['MQL', 'SQL', 'Demo', 'Closed Won']
    funnel_counts = leads['status'].value_counts().reindex(stages_order).fillna(0)
    
    # Plotting the horizontal bar chart (Funnel)
    plt.figure(figsize=(10, 6))
    colors = sns.color_palette("Blues_r", len(stages_order))
    
    bars = plt.barh(stages_order[::-1], funnel_counts[::-1], color=colors)
    plt.title('Sales Funnel Efficiency: AllStarsIT', fontsize=14, pad=20)
    plt.xlabel('Number of Leads')
    
    # Add numeric labels to bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 2, bar.get_y() + bar.get_height()/2, 
                 f'{int(width)}', va='center', fontweight='bold')
    
    plt.tight_layout()
    ensure_dir('images')
    plt.savefig('images/sales_funnel.png')
    print("✓ Sales funnel chart saved to images/sales_funnel.png")

def plot_marketing_roi(roi_df):
    """Visualizes Revenue vs Ad Spend comparison."""
    plt.figure(figsize=(10, 6))
    
    # Setting country as index for side-by-side plotting
    roi_df.set_index('country')[['monthly_revenue', 'total_ads_spend']].plot(
        kind='bar', color=['#2ecc71', '#e74c3c'], ax=plt.gca()
    )
    
    plt.title('Revenue (MRR) vs Marketing Budget by Country', fontsize=12)
    plt.ylabel('Amount in USD ($)')
    plt.xticks(rotation=0)
    plt.legend(['Monthly Revenue', 'Ad Spend'])
    
    plt.tight_layout()
    ensure_dir('images')
    plt.savefig('images/marketing_roi.png')
    print("✓ ROI chart saved to images/marketing_roi.png")

if __name__ == "__main__":
    print("--- Executing Business Analytics Suite ---")
    
    # Paths to your CSV data (generated via Mockaroo)
    # To run this locally, ensure the 'data' folder contains these files:
    
    # try:
    #     # RAM Automation Case
    #     roi_results = analyze_ram_performance('data/ram_subscriptions.csv', 'data/ram_marketing.csv')
    #     plot_marketing_roi(roi_results)
    #
    #     # AllStarsIT Case
    #     visualize_sales_funnel('data/allstars_leads.csv')
    #
    #     print("\nSuccess: Analytics and Visualizations are ready for the README.")
    # except Exception as e:
    #     print(f"\n[Error]: {e}")
    #     print("Please ensure your CSV files are in the 'data/' folder.")

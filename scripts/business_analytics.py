import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Visual settings for professional reporting
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 100

def ensure_dir(directory):
    """Creates directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def analyze_ram_roi(subs_path, marketing_path):
    """
    RAM Automation Case:
    Matches SQL Analysis: Revenue vs Spend by Country.
    """
    try:
        # Load data
        subs = pd.read_csv(subs_path)
        marketing = pd.read_csv(marketing_path)
        
        # Filtering only active customers (WHERE churned = false)
        active_subs = subs[subs['churned'] == False].copy()
        
        # Aggregating monthly revenue by country
        revenue_df = active_subs.groupby('country')['monthly_revenue'].sum().reset_index()
        
        # Merging with marketing costs (JOIN s.country = m.country)
        roi_df = pd.merge(revenue_df, marketing, on='country')
        
        # Calculating ROI ratio
        roi_df['roi_ratio'] = (roi_df['monthly_revenue'] / roi_df['total_ads_spend']).round(2)
        
        return roi_df
    except Exception as e:
        print(f"Error in RAM analysis: {e}")
        return None

def visualize_allstars_funnel(leads_path):
    """
    AllStarsIT Case:
    Visualizes lead distribution using your specific sales stages.
    """
    try:
        leads = pd.read_csv(leads_path)
        
        # Definining the funnel stages in logical order
        stages_order = [
            'New', 
            'Marketing Qualified Lead', 
            'Sales Qualified Lead', 
            'In Process'
        ]
        
        # Count occurrences of each status and reindex to match the order
        funnel_counts = leads['status'].value_counts().reindex(stages_order).fillna(0)
        
        plt.figure(figsize=(12, 7))
        colors = sns.color_palette("viridis", len(stages_order))
        
        # Creating a horizontal bar chart
        bars = plt.barh(stages_order[::-1], funnel_counts[::-1], color=colors)
        plt.title('Sales Funnel Distribution: AllStarsIT', fontsize=14, pad=20)
        plt.xlabel('Number of Leads')
        
        # Adding labels with the count of leads on each bar
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                     f'{int(width)}', va='center', fontweight='bold')
        
        plt.tight_layout()
        ensure_dir('images')
        plt.savefig('images/sales_funnel.png')
        print("✓ Successfully saved: images/sales_funnel.png")
    except Exception as e:
        print(f"Error in AllStars funnel visualization: {e}")

def plot_ram_roi(roi_df):
    """Creates a comparison chart: Revenue vs Marketing Budget."""
    if roi_df is None: return
    
    plt.figure(figsize=(10, 6))
    
    # Comparing revenue and spend side-by-side
    roi_df.set_index('country')[['monthly_revenue', 'total_ads_spend']].plot(
        kind='bar', color=['#2ecc71', '#e74c3c'], ax=plt.gca()
    )
    
    plt.title('RAM Automation: Revenue vs Marketing Spend', fontsize=12)
    plt.ylabel('Amount in USD ($)')
    plt.xticks(rotation=0)
    plt.legend(['Total Revenue', 'Ad Spend'])
    
    plt.tight_layout()
    ensure_dir('images')
    plt.savefig('images/marketing_roi.png')
    print("✓ Successfully saved: images/marketing_roi.png")

if __name__ == "__main__":
    print("--- Starting Python Business Analytics ---")
    
    # Files expected in the /data folder
    RAM_SUBS = 'data/ram_subscriptions.csv'
    RAM_MARKETING = 'data/ram_marketing_costs.csv'
    ALLSTARS_LEADS = 'data/allstars_leads.csv'
    
    # 1. Run RAM ROI Analysis
    ram_data = analyze_ram_roi(RAM_SUBS, RAM_MARKETING)
    plot_ram_roi(ram_data)
    
    # 2. Run AllStars Sales Funnel Analysis
    visualize_allstars_funnel(ALLSTARS_LEADS)
    
    print("\nProcessing complete. Check the 'images/' folder for visualizations.")

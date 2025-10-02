#!/usr/bin/env python3

"""seaborn-charts.py here.

Create chart for the data side-by-side using plt.subplots().
"""

__last_change__ = "25-10-02 v013 + Side-by-Side Plotting"


# Internal imports (no pip/uv add needed):
from datetime import datetime, timezone
import sys

try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import statsmodels.multivariate.manova as manova    
    
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    sys.exit(9)

# --- Configuration & Helpers ---

# Adjust figure size for side-by-side display (e.g., width doubled)
FIGURE_SIZE = (18, 7)
FONT_SIZE = {
    'title': 14,
    'label': 12,
    'annotate': 10,
    'overlay': 18,
    'datestamp': 8,
    'manova': 10,
}
POINT_SIZES = (50, 200)

def add_annotations(ax, df, formatted_time, f_value, p_value, is_first_plot):
    """Add standard annotations (text, MNOVA, LLM names, trendline) to a given axis."""
    # Define columns based on plot type
    x_col = 'MilliSecs' if is_first_plot else 'Accuracy'
    y_col = 'USD cents'

    # Datestamp
    ax.text(
        0.80, .90, formatted_time,
        horizontalalignment='right', verticalalignment='bottom',
        transform=ax.transAxes, fontsize=FONT_SIZE['datestamp'], color='grey'
    )
    
    # Overlay Text (Not Worth It!)
    ax.text(
        0.80, 0.80, "Not Worth It!",
        horizontalalignment='right', fontstyle='italic', verticalalignment='bottom',
        transform=ax.transAxes, fontsize=FONT_SIZE['overlay'], color='#F08080'
    )
    
    # Overlay Text (Bargain!)
    ax.text(
        0.20, 0.20, 'Bargain!',
        horizontalalignment='right', verticalalignment='bottom', fontstyle='italic',
        transform=ax.transAxes, fontsize=FONT_SIZE['overlay'], color='#006400'
    )
    
    # MNOVA Results (Shown only on the first plot)
    if is_first_plot:
        ax.text(
            0.05, 0.95, f"F={f_value:.2f} p={p_value:.2f}",
            transform=ax.transAxes, fontsize=FONT_SIZE['manova'], verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='none', alpha=0.7)
        )
        
    # Trendline (Regression Plot)
    sns.regplot(data=df, x=x_col, y=y_col, scatter=False, ci=None, 
                color='grey', line_kws={'linestyle': '--'}, ax=ax)

    # Dynamically label each point with the LLM name
    for _, row in df.iterrows():
        ax.annotate(
            text=row['LLM'],
            xy=(row[x_col], row[y_col]),
            xytext=(7, 0), # Reduced offset for subplots
            textcoords='offset points',
            ha='left',
            fontsize=FONT_SIZE['annotate']
        )
        
def plot_chart(ax, df, formatted_time, f_value, p_value, is_first_plot):
    """Create one of the two charts on a specified axis (ax)."""
    # Setup plot-specific titles and labels
    if is_first_plot:
        x_col, hue_col, title, x_label, legend_title = (
            'MilliSecs', 'Accuracy', '4D-LLM Eval: Cost vs Accuracy vs Speed Scatter Plot', 
            'Milliseconds response time', 'Accuracy'
        )
    else:
        # Second Plot (Accuracy vs Cost, colored by MilliSecs)
        x_col, hue_col, title, x_label, legend_title = (
            'Accuracy', 'MilliSecs', '4D-LLM Eval: Cost vs Accuracy Scatter Plot', 
            'Accuracy %', 'Speed (MilliSecs)'
        )

    # Main Scatter Plot
    # Sorting ensures consistent point and legend order
    df.sort_values("Accuracy", ascending=False, inplace=True)
    sns.scatterplot(
        data=df, x=x_col, y='USD cents', markers=True, 
        hue=hue_col, edgecolor='black', size='CoV', 
        sizes=POINT_SIZES, palette='RdYlGn', ax=ax
    )

    # Set Titles and Labels
    ax.set_title(title, fontsize=FONT_SIZE['title'])
    ax.set_xlabel(x_label)
    ax.set_ylabel('USD cents cost')
    
    # Styling and Legend
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    sns.despine(ax=ax, trim=True, offset=5)

    # Customize the Legend (outside the plot area)
    ax.legend(
        bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0., title=legend_title
    )
    
    # Add all other annotations
    add_annotations(ax, df, formatted_time, f_value, p_value, is_first_plot)

    # **NEW: REVERSE X-AXIS FOR THE SECOND PLOT**
    if not is_first_plot:
        ax.invert_xaxis()


# --- Main Execution ---

if __name__ == '__main__':
    
    # Data Loading
    try:
        df = pd.read_csv('seaborn-charts.csv')
    except FileNotFoundError:
        print("Error: 'seaborn-charts.csv' not found. Please ensure the file exists.")
        sys.exit(1)
        
    # Pre-calculations
    formatted_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Calculate MNOVA values
    dfs = df[['Accuracy','USD cents']]
    manova_result = manova.MANOVA.from_formula('dfs ~ MilliSecs', data=df)
    results = manova_result.mv_test()
    f_value = results.results['MilliSecs']['stat']['F Value'].iloc[0]
    p_value = results.results['MilliSecs']['stat']['Pr > F'].iloc[0] 

    # **CORE CHANGE: Create Figure and Axes for Side-by-Side Plots**
    # 1 row, 2 columns. axes[0] for the first plot, axes[1] for the second.
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZE)
    sns.set_theme(style='darkgrid')

    # Plot Generation
    # Use .copy() to prevent modifying the DataFrame in a way that affects the other plot
    plot_chart(axes[0], df.copy(), formatted_time, f_value, p_value, is_first_plot=True)
    plot_chart(axes[1], df.copy(), formatted_time, f_value, p_value, is_first_plot=False)

    # Final Display
    plt.tight_layout(rect=[0, 0, 1, 1]) # Adjusts plots to fit figure, accounting for legends
    plt.show()
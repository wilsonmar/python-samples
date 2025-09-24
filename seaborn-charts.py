#!/usr/bin/env python3

"""seaborn-charts.py here.

Create chart for the data.

https://github.com/wilsonmar/python-samples/blob/main/seaborn-charts.py

Before running this:
    chmod +x seaborn-charts.py

# TODO:
[ ] Remove millisecs legend
Sort Accuracy legend, green on top
Title to LLM Eval: Cost vs Accuracy vs Speed Scatter Plot
Bargain! & Not worth it! overlay? text

"""
__last_change__ = "25-09-21 v007 + chg Cohere pos. add CoE :seaborn-charts.py"

# Internal imports (no pip/uv add needed):
from datetime import datetime, timezone

try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import statsmodels.multivariate.manova as manova    
    
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)

#Read data from a CSV file into a pandas DataFrame
df = pd.read_csv('python-samples-llms.csv')
# Change figure size
# This must be done BEFORE creating the plot. Control your chart size.
plt.figure(figsize=(10, 6))
# Ensure 'x_column' and 'y_column' exist in your CSV file
sns.set_theme(style='darkgrid')
# Get the colors from a Seaborn palette
#palette = sns.color_palette("RdYlGn_r", as_cmap=False, n_colors=len(df['Accuracy'].unique()))
#color_map = {category: color for category, color in zip(df['Accuracy'].unique(), palette)}
#edge_colors = df['Accuracy'].map(color_map).values

#Get the current UTC time
current_utc_time = datetime.now(timezone.utc)
formatted_time = current_utc_time.strftime('%Y-%m-%d %H:%M:%S UTC')
# The 'transform=plt.gca().transAxes' places the text relative to the axes
plt.text(
    0.95,  # x-position (0.0 to 1.0)
    0.95,  # y-position (0.0 to 1.0)
    formatted_time,
    horizontalalignment='right',
    verticalalignment='bottom',
    transform=plt.gca().transAxes,
    fontsize=8,
    color='grey'
)
plt.text(
    0.80,  # x-position (0.0 to 1.0)
    0.80,  # y-position (0.0 to 1.0)
    "Not Worth It!",
    horizontalalignment='right',
    verticalalignment='bottom',
    transform=plt.gca().transAxes,
    fontsize=18,
    color='#F08080'
)
plt.text(
    0.20,  # x-position (0.0 to 1.0)
    0.20,  # y-position (0.0 to 1.0)
    'Bargain!',
    horizontalalignment='right',
    verticalalignment='bottom',
    transform=plt.gca().transAxes,
    fontsize=18,
    color='#006400'
)

#change edge color and size of marker by changing s values
df.sort_values("Accuracy", ascending=False, inplace=True)
#ax=sns.scatterplot(data=df, x='MilliSecs', y='USD cents',markers=True,ls='-',color='cornflowerblue',hue='Accuracy',legend='auto',edgecolor='black',sizes=(50,200),size='MilliSecs',palette='RdYlGn')
ax=sns.scatterplot(data=df, x='MilliSecs', y='USD cents',markers=True,ls='-',color='cornflowerblue',hue='Accuracy',legend='auto',edgecolor='black',size='Accuracy',sizes=(50,200),palette='RdYlGn') # RdYlGn_r reverses the order
ax=sns.regplot(data=df, x='MilliSecs', y='USD cents', ax=ax, scatter=False, ci=None, color='grey',line_kws={'linestyle': '--'})


#Add plot titles and labels for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.set_title('LLM Eval: Cost vs Accuracy vs Speed Scatter Plot', fontsize=16)
plt.xlabel('Milliseconds response time')
plt.ylabel('USD cents cost')
sns.despine(trim=True, offset=5)
#Customize the Legend
plt.legend(title='Accuracy') # Adds a legend for the size

# Dynamically label each point with the LLM name
for index, row in df.iterrows():
    # Place text to the right of each point
    plt.annotate(
        text=row['LLM'],           # Use the LLM name as the label
        xy=(row['MilliSecs'], row['USD cents']),
        xytext=(10, 0),              # Offset the text by 10 points to the right
        textcoords='offset points',
        ha='left',                   # Align the text to the left
        #arrowprops=dict(arrowstyle='', color='gray') # Optional arrow
    )

# Calculate MNOVA values
dfs=df[['Accuracy','USD cents']]# Dependent variables
Accuracy_Group=df[['MilliSecs']]# Independent variables
manova_result = manova.MANOVA.from_formula('dfs ~ Accuracy_Group', data=df)
results=manova_result.mv_test()
f_value = results.results['Accuracy_Group']['stat']['F Value'][0]# Get the F-value from Wilken's Lambda test
p_value = results.results['Accuracy_Group']['stat']['Pr > F'][0]  # Get the p-value from Wilken's Lambda test
# Add text using ax.text()
ax.text(
    0.25,  # X-coordinate (5% from the left)
    0.50,  # Y-coordinate (95% from the bottom)
    f"F={f_value:.2f} p={p_value:.2f}",#f"F:{f_value:.2f} p={p_value:.3f}",  # Text to display
    transform=ax.transAxes, # Use axes coordinates
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='none', alpha=0.7)
)
#Display the plot
plt.tight_layout() # Adjusts plot to fit figure
plt.show()
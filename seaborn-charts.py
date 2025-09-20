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
__last_change__ = "25-09-20 v003 + from pip to uv :seaborn-charts.py"

# Internal imports (no pip/uv add needed):
from datetime import datetime, timezone

try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)

#Read data from a CSV file into a pandas DataFrame
df = pd.read_csv('python-samples-llms.csv')

# Change figure size
# This must be done BEFORE creating the plot. Control your chart size.
plt.figure(figsize=(10, 6))
#fig, ax = plt.subplots()
#Create a Seaborn lineplot
# Ensure 'x_column' and 'y_column' exist in your CSV file
sns.set_theme(style='darkgrid')

# Get the colors from a Seaborn palette
palette = sns.color_palette("viridis", as_cmap=False, n_colors=len(df['Accuracy'].unique()))

# Map the 'z' column to the colors
color_map = {category: color for category, color in zip(df['Accuracy'].unique(), palette)}
edge_colors = df['Accuracy'].map(color_map).values

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
#change edge color and size of marker by chaging s values
ax=sns.scatterplot(data=df, x='MilliSecs', y='USD cents',markers=True,ls='-',color='cornflowerblue',hue='Accuracy',legend='auto',edgecolor='black',sizes=(50,200),size='MilliSecs')
ax=sns.regplot(data=df, x='MilliSecs', y='USD cents', ax=ax, scatter=False, ci=None, color='grey',line_kws={'linestyle': '--'})

#Add plot titles and labels for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)
#Customize the Legend
ax.set_title('LLM Eval: Cost vs Accuracy vs Speed Scatter Plot', fontsize=16)
plt.xlabel('Milliseconds response time')
plt.ylabel('USD cents cost')
sns.despine(trim=True, offset=5)
#plt.legend(title='Note') # Adds a legend for the size

#Display the plot
plt.tight_layout() # Adjusts plot to fit figure
plt.show()
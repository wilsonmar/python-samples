#!/usr/bin/env python3

"""seaborn-charts.py here.

Create chart for the data.

https://github.com/wilsonmar/python-samples/blob/main/seaborn-charts.py

Before running this:
    chmod +x seaborn-charts.py
    
In Window machine command prompt:
    python seaborn-charts.py
In Mac/Linux command line:
    ./seaborn-charts.py
Requires:
    pip install pandas seaborn matplotlib statsmodels
    

# TODO:
[ ] Remove millisecs legend- Done
Sort Accuracy legend, green on top
Title to LLM Eval: Cost vs Accuracy vs Speed Scatter Plot - Done
Bargain! & Not worth it! overlay? text - Done
[ ] Add MNOVA results to chart - Done
[ ] Add trendline - Done
2nd chart with size by cost, color by accuracy- Done
Can we make the comments "Not Worth It!" and "Bargain!" in italics?- Done
Can we make the font larger for all chars? - Done
Can the legend be on the right on both plots? -Done

"""
__last_change__ = "25-09-29 v011  +  2nd chart legend hyphen fixed  :seaborn-charts.py"


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
df = pd.read_csv('seaborn-charts.csv')
# Change figure size
# This must be done BEFORE creating the plot. Control your chart size.
plt.figure(figsize=(10, 6))
# Ensure 'x_column' and 'y_column' exist in your CSV file
sns.set_theme(style='darkgrid')

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
    fontstyle='italic',
    verticalalignment='bottom',
    transform=plt.gca().transAxes,
    fontsize=22,
    color='#F08080'
)
plt.text(
    0.20,  # x-position (0.0 to 1.0)
    0.20,  # y-position (0.0 to 1.0)
    'Bargain!',
    horizontalalignment='right',
    verticalalignment='bottom',
    fontstyle='italic',
    transform=plt.gca().transAxes,
    fontsize=22,
    color='#006400'
)
# Create a first chart

#change edge color and size of marker by changing s values
df.sort_values("Accuracy", ascending=False, inplace=True)
ax=sns.scatterplot(data=df, x='MilliSecs', y='USD cents',markers=True,color='cornflowerblue',hue='Accuracy',edgecolor='black',size='CoV',sizes=(50,200),palette='RdYlGn') # RdYlGn_r reverses the order
ax=sns.regplot(data=df, x='MilliSecs', y='USD cents', scatter=False, ci=None, color='grey',line_kws={'linestyle': '--'})


#Add plot titles and labels for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.set_title('LLM Eval: Cost vs Accuracy vs Speed Scatter Plot', fontsize=22)
plt.xlabel('Milliseconds response time')
plt.ylabel('USD cents cost')
sns.despine(trim=True, offset=5)
#Customize the Legend
# Place the legend outside the plot area
plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    borderaxespad=0.
    )
# Dynamically label each point with the LLM name
for index, row in df.iterrows():
    # Place text to the right of each point
    plt.annotate(
        text=row['LLM'],           # Use the LLM name as the label
        xy=(row['MilliSecs'], row['USD cents']),
        xytext=(10, 0),              # Offset the text by 10 points to the right
        textcoords='offset points',
        ha='left',                   # Align the text to the left
         fontsize=12
        #arrowprops=dict(arrowstyle='', color='gray') # Optional arrow
    )

# Calculate MNOVA values
#https://in.mathworks.com/discovery/manova.html for context 
#https://online.stat.psu.edu/stat505/book/export/html/762 and https://www.statsmodels.org/dev/_modules/statsmodels/multivariate/manova.html
dfs=df[['Accuracy','USD cents']]# Dependent variables
Accuracy_Group=df[['MilliSecs']]# Independent variables
manova_result = manova.MANOVA.from_formula('dfs ~ Accuracy_Group', data=df)
results=manova_result.mv_test()
f_value = results.results['Accuracy_Group']['stat']['F Value'].iloc[0]# Get the F-value from Wilken's Lambda test
p_value = results.results['Accuracy_Group']['stat']['Pr > F'].iloc[0]  # Get the p-value from Wilken's Lambda test
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

# Create a second chart
plt.figure(figsize=(10, 6))
# Ensure 'x_column' and 'y_column' exist in your CSV file
sns.set_theme(style='darkgrid')
df.sort_values("Accuracy", ascending=False, inplace=True)
ax=sns.scatterplot(data=df, x='Accuracy', y='USD cents',markers=True,color='cornflowerblue',hue='CoV',edgecolor='black',size='CoV',sizes=(50,200),palette='RdYlGn') # RdYlGn_r reverses the order
ax=sns.regplot(data=df, x='Accuracy', y='USD cents', scatter=False, ci=None, color='grey',line_kws={'linestyle': '--'})

#Add plot titles and labels for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)

ax.set_title('LLM Eval: Cost vs Accuracy Scatter Plot', fontsize=22)
plt.xlabel('Accuracy %')
plt.ylabel('USD cents cost')
sns.despine(trim=True, offset=5)
#Customize the Legend
# Place the legend outside the plot area
plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    borderaxespad=0.,
    title='Accuracy'
)
# Dynamically label each point with the LLM name
for index, row in df.iterrows():
    # Place text to the right of each point
    plt.annotate(
        text=row['LLM'],           # Use the LLM name as the label
        xy=(row['Accuracy'], row['USD cents']),
        xytext=(10, 0),              # Offset the text by 10 points to the right
        textcoords='offset points',
        ha='left',                   # Align the text to the left
        fontsize=12
        #arrowprops=dict(arrowstyle='', color='gray') # Optional arrow
    )
ax.text(
    0.25,  # X-coordinate (5% from the left)
    0.50,  # Y-coordinate (95% from the bottom)
    f"F={f_value:.2f} p={p_value:.2f}",#f"F:{f_value:.2f} p={p_value:.3f}",  # Text to display
    transform=ax.transAxes, # Use axes coordinates
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='none', alpha=0.7)
)
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
#Display the plot
plt.tight_layout() # Adjusts plot to fit figure
plt.show()
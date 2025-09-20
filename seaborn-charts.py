"""Create chart for the data."""

__last_change__ = "25-09-20 v001 + regression line,dynamic size of points added :seaborn-charts.py"

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
palette = sns.color_palette("viridis", as_cmap=False, n_colors=len(df['Output'].unique()))

# Map the 'z' column to the colors
color_map = {category: color for category, color in zip(df['Output'].unique(), palette)}
edge_colors = df['Output'].map(color_map).values

#change edge color and size of marker by chaging s values

ax=sns.scatterplot(data=df, x='MilliSecs', y=' USD cents ',markers=True,ls='-',color='cornflowerblue',hue='Output',legend='auto',edgecolor='black',sizes=(50,200),size='MilliSecs')
ax=sns.regplot(data=df, x='MilliSecs', y=' USD cents ', ax=ax, scatter=False, ci=None, color='red')
#Add plot titles and labels for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)
#Customize the Legend
ax.set_title('Cost of LLM / Dollar', fontsize=16)
plt.xlabel('Millisecs response time')
plt.ylabel('USD cents cost')
sns.despine(trim=True, offset=5)
#plt.legend(title='Note') # Adds a legend for the size

#Display the plot
plt.tight_layout() # Adjusts plot to fit figure
plt.show()
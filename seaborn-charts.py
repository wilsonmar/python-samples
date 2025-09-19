"""Create chart for the data."""



try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
except Exception as e:
    print(f"Python module import failed: {e}")
    print("Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)

#Read data from a CSV file into a pandas DataFrame
df = pd.read_csv('your_data.csv')

# Change figure size
# This must be done BEFORE creating the plot. Control your chart size.
plt.figure(figsize=(10, 6))

#Create a Seaborn lineplot
# Ensure 'x_column' and 'y_column' exist in your CSV file
sns.set_theme(style='darkgrid')
# Get the colors from a Seaborn palette
palette = sns.color_palette("viridis", as_cmap=False, n_colors=len(df['Run_Id'].unique()))

# Map the 'z' column to the colors
color_map = {category: color for category, color in zip(df['Run_Id'].unique(), palette)}
edge_colors = df['Run_Id'].map(color_map).values

#change edge color and size of marker by chaging s values
ax=sns.scatterplot(data=df, x='US_Dollars', y='LLM',markers=True,ls='-',color='cornflowerblue',hue='Accuracy',legend='auto',edgecolor='black',s=100)

#Add plot titles and labels for clarity
plt.grid(axis='y', linestyle='--', alpha=0.7)
#Customize the Legend
ax.set_title('Cost of LLM / Dollar / Day', fontsize=16)
plt.xlabel('Dollar spent / cents')
plt.ylabel('Name of the LLM')
sns.despine(trim=True, offset=5)

#Display the plot
plt.tight_layout() # Adjusts plot to fit figure
plt.show()
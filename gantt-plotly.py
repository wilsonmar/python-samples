#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Unlike regular comments, docstrings are available at runtime to the compiler:
# 2025-07-30 
__last_commit__ = "v007 rename from gantt-chart.py :gantt-plotly.py"

"""Gantt chart generation module.

This module provides functions to generate both static and interactive Gantt charts
using matplotlib and plotly libraries.

Based on Hari Sekhon's work.
See https://github.com/HariSekhon/GitHub-Repos-MermaidJS-Gantt-Chart
and https://github.com/HariSekhon/Diagrams-as-Code

The GitHub API is used to obtain the list of repositories.
The MermaidJS generates the Gantt chart graphic.
Graphwiz renders the Gantt chart graphic.

The init.mmd file contains the initialization code to specific formatting.
"""

from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def static_gantt_chart():
    """Generate static Gantt Chart."""
    df = pd.DataFrame({
        'task': ['A', 'B', 'C'],
        'start': pd.to_datetime(['2025-07-10', '2025-07-15', '2025-07-20']),
        'end': pd.to_datetime(['2025-07-14', '2025-07-18', '2025-07-23'])
    })

    # Calculate days from the minimum start date for each task
    df['days_to_start'] = (df['start'] - df['start'].min()).dt.days
    df['task_duration'] = (df['end'] - df['start']).dt.days + 1

    plt.barh(df['task'], df['task_duration'], left=df['days_to_start'])
    plt.xlabel('Days')
    plt.ylabel('Tasks')
    plt.title('Gantt Chart')
    plt.show()


def interactive_gantt_chart():
    """Open an interactive Gantt chart in a new tab.
    
    Opens default browser app (from localhost:61106) to display Plotly timeline chart.
    """
    # from io import StringIO
    # import pandas as pd
    # import plotly.express as px

    # TODO: Load DataFrame from CSV file:
    csv_string = "Task,Start,End\nA,2025-07-10,2025-07-14\nB,2025-07-15,2025-07-18\nC,2025-07-20,2025-07-23"
    df = pd.read_csv(StringIO(csv_string))
    # print(df)
       #   Task       Start         End
       # 0    A  2025-07-10  2025-07-14
    """
    df = pd.DataFrame([
        dict(Task="A", Start='2025-07-10', End='2025-07-14'),
        dict(Task="B", Start='2025-07-15', End='2025-07-18'),
        dict(Task="C", Start='2025-07-20', End='2025-07-23'),
    ])
    """
    # TODO: Sort from A down.
    fig = px.timeline(df, x_start="Start", x_end="End", y="Task")
    fig.update_yaxes(autorange="reversed")  # Earliest task at the top
    try:
        fig.show()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")


if __name__ == '__main__':
    interactive_gantt_chart()
    # static_gantt_chart()
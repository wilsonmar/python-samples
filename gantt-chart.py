#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gantt chart generation module.

This module provides functions to generate both static and interactive Gantt charts
using matplotlib and plotly libraries.
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Unlike regular comments, docstrings are available at runtime to the compiler:
__last_commit__ = "v004 + docstring :gantt-chart.py"

""" gantt-chart.py

within https://github.com/wilsonmar/python-samples/blob/main/gantt-chart.py

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
   OF ANY KIND, either express or implied. See the License for the specific
   language governing permissions and limitations under the License.

Based on Hari Sekhon's work.
See https://github.com/HariSekhon/GitHub-Repos-MermaidJS-Gantt-Chart
and https://github.com/HariSekhon/Diagrams-as-Code
    * The GitHub API is used to obtain the list of repositories.
    * The MermaidJS generates the Gantt chart graphic
    * Graphwiz renders the Gantt chart graphic

The <tt>init.mmd</tt> file contains the initialization code to specific formatting.

%%{ init: {
        "logLevel": "debug",
        'theme': 'dark',
        'themeVariables': {
          'activeTaskBkgColor': '#0000ff',
          'activeTaskBorderColor': 'lightgrey',
          'critBorderColor': 'lightgrey',
          'doneTaskBkgColor': 'grey',
          'doneTaskBorderColor': 'lightgrey',
          'taskBkgColor': 'black',
          'taskBorderColor': 'black',
          'taskTextColor': 'white',
          'taskTextDarkColor': 'white',
          'taskTextLightColor': 'black',
          'todayLineColor': 'red'
        }
    }
}%%
gantt
    dateFormat  YYYY-MM-DD
    title Repositories Gantt Chart
    Nagios-Plugins : active, 2012-12-30, 2024-09-22
    lib : active, 2012-12-30, 2024-09-22
    Spotify-tools : active, 2012-12-30, 2024-09-22
    DevOps-Perl-tools : active, 2012-12-30, 2024-09-22
    spark-apps : done, 2015-05-25, 2020-04-02
    lib-java : active, 2015-05-31, 2024-09-22
    pylib : active, 2015-10-27, 2024-09-23
    DevOps-Python-tools : active, 2015-10-27, 2024-09-23
    Dockerfiles : active, 2016-01-17, 2024-09-28
    DevOps-Bash-tools : active, 2016-01-17, 2024-09-28
    Nagios-Plugin-Kafka : active, 2016-06-07, 2024-09-22
    HAProxy-configs : active, 2018-06-08, 2024-09-22
    DevOps-Golang-tools : active, 2020-04-30, 2024-09-22
    Spotify-Playlists : active, 2020-06-29, 2024-09-22
    SQL-scripts : active, 2020-08-05, 2024-09-21
    Kubernetes-configs : active, 2020-09-16, 2024-09-21
    SQL-keywords : active, 2020-09-16, 2024-09-21
    Templates : active, 2020-09-16, 2024-09-25
    TeamCity-CI : active, 2020-12-03, 2024-09-21
    Terraform : active, 2021-01-18, 2024-09-21
    Jenkins : active, 2022-01-17, 2024-09-23
    GitHub-Actions : active, 2022-01-17, 2024-09-22
    CI-CD : active, 2022-03-25, 2024-10-01
    GitHub-Actions-Contexts : active, 2022-08-17, 2024-09-21
    Diagrams-as-Code : active, 2023-04-14, 2024-10-02
    Template-Repo : active, 2023-04-15, 2024-09-22
    Packer : active, 2023-06-02, 2024-09-21
    Vagrant-templates : active, 2023-06-12, 2024-09-21
    Knowledge-Base : active, 2023-11-22, 2024-09-29
    HariSekhon : active, 2024-08-14, 2024-10-02
    GitHub-Commit-Times-Graph : active, 2024-09-07, 2024-09-08
    GitHub-Repos-MermaidJS-Gantt-Chart : active, 2024-10-02, 2024-10-02
}
uv run gantt-chart.py
"""

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
    
    Opens an interactive Gantt chart in a new tab on default browser app 
    (from localhost:61106).
    """
    # import pandas as pd
    # import plotly.express as px

    # TODO: Load DataFrame from CSV file:
    df = pd.DataFrame([
        dict(Task="A", Start='2025-07-10', End='2025-07-14'),
        dict(Task="B", Start='2025-07-15', End='2025-07-18'),
        dict(Task="C", Start='2025-07-20', End='2025-07-23'),
    ])

    fig = px.timeline(df, x_start="Start", x_end="End", y="Task")
    fig.update_yaxes(autorange="reversed")  # Earliest task at the top
    try:
        fig.show()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")


if __name__ == '__main__':
    interactive_gantt_chart()
    # static_gantt_chart()
#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

"""scan-bad.py at https://github.com/wilsonmar/python-samples/blob/main/scan-bad.py

This program loads a list of words from a CSV file and 
checks if any of the words are present in the input string specified.

# Based on https://www.perplexity.ai/search/write-a-python-cli-program-to-CIbauWQ9RASqhNONcHy28Q#0

1. In Terminal: one time to initialize run environment:
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install typer
    chmod +x scan-bad.py
2. Sample run command containing text to check
    ./scan-bad.py "advocate for children" scan-ban.csv
"""
import csv

try:
    import typer
except Exception as e:
    print(f"Python module import failed: {e}")
    print(f"Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate")
    exit(9)

app = typer.Typer()

def load_words_from_csv(file_path):
    words = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            words.extend(row)
    return words

@app.command()
def check_words(input_string: str, csv_file: str):
    """
    Check if the input string contains any words from the CSV file.
    """
    word_list = load_words_from_csv(csv_file)
    
    found_words = [word for word in word_list if word.lower() in input_string.lower()]
    
    if found_words:
        typer.echo(f"The input string contains the following words from the list: {', '.join(found_words)}")
    else:
        typer.echo("The input string does not contain any words from the list.")

if __name__ == "__main__":
    app()


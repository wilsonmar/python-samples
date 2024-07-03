#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
"""
This is surprise.py at 
https://github.com/wilsonmar/python-samples/blob/main/recommender/surpirsepy
   Not yet explained at https://wilsonmar.github.io/python-samples 
   Based on https://hackr.io/blog/python-projects

This program provides a GUI created (using tkinter) to select movies and TV shows as an example of data science machine learning. See https://hackr.io/blog/python-concepts-data-science

"""

# Needs pip install:
from surprise import Dataset, SVD
from surprise.model_selection import cross_validate


# Load the movielens-100k dataset (download it if needed),
data = Dataset.load_builtin("ml-100k")

# We'll use the famous SVD algorithm.
algo = SVD()

# Run 5-fold cross-validation and print results
cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)
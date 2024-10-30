#!/usr/bin/env python3

""" sklearn-sample.py

This generates random then uses Sklean to calculate 
the average squared difference between predicted and actual values.
for Logistic Regression and # KNN (K-Nearest Neighbors)
MAE (Mean Square Error) and MSE (Mean Absolute Error).
MAE is calculated as the average of the absolute differences between the predicted values and the actual values.
MSE is also known as the L2 norm or the Euclidean distance
which gives more weight to larger errors than smaller ones, thus penalizing outliers more harshly. 
But it can also make MSE sensitive to noise and skewness in the data
MAE is robust to outliers, providing a stable average error measure.
See https://www.linkedin.com/advice/0/what-difference-between-mean-squared-error-tz1mc

TODO: Add confusion Matrix & Evaluation Metrics?

"""

# conda install --name py313 numpy scikit-learn
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

# Alt: For pytorch see https://www.v7labs.com/blog/performance-metrics-in-machine-learning

# Globals:
DEBUGGING = True

GEN_RANDOM = True
TEST_SIZE_RATIO = 0.3

# Main:

if GEN_RANDOM:
    # Generate sample data randomly:
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    # TODO: Choice of Randomness weighted toward TP, TN, etc.
if DEBUGGING:
    print(f"X=np.random.rand(100,5)={X}")
    print(f"y=np.random.randint={y}")

# STEP: Split data into k-folds:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_RATIO)
    # TODO: Create a fold for validation as well ans Testing & Training.

# STEP: Calculate Logistic Regression:
lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# STEP: Calculate errors for Logistic Regression:
mae_lr = metrics.mean_absolute_error(y_test, y_pred_lr)
    # MAE measures the average magnitude of errors between predicted and actual values
    # (by squaring to remove consideration of the direction of error).
    # MAE is especially useful in applications that aim to minimize the average error and
    # is less sensitive to outliers than other metrics like Mean Squared Error (MSE).

mse_lr = metrics.mean_squared_error(y_test, y_pred_lr)

# STEP: Calculate KNN (K-Nearest Neighbors):
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

# STEP: Calculate errors for KNN:
mae_knn = metrics.mean_absolute_error(y_test, y_pred_knn)
mse_knn = metrics.mean_squared_error(y_test, y_pred_knn)
# TODO: RMSE (Root Mean Squared Error) https://www.analyticsvidhya.com/blog/2019/08/11-important-model-evaluation-error-metrics/#Root_Mean_Squared_Error_(RMSE)

# Probability output for Algorithms like Logistic Regression, Random Forest, Gradient Boosting, Adaboost, etc.,
# give probability outputs. Converting probability outputs to class output is a matter of
# creating a threshold probability.
print(f"Logistic Regression (of continuous numerical values):\nMAE: {mae_lr:.4f}, \nMSE: {mse_lr:.4f}")

# Class output for algorithms like SVM and KNN. For instance,
# in a binary classification problem, the outputs will be either 0 or 1.
# However, today we have algorithms that can convert these class outputs to probability.
# But these algorithms are not well accepted by the statistics community.
print(f"KNN (K-Nearest Neighbors) of discret classification:\nMAE: {mae_knn:.4f}, \nMSE: {mse_knn:.4f}")

""" Sample output:
Logistic Regression:
MAE: 0.5000,
MSE: 0.5000
KNN (K-Nearest Neighbors):
MAE: 0.5333,
MSE: 0.5333
"""
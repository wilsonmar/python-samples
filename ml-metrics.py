#!/usr/bin/env python3

""" ml-metrics.py at https://github.com/wilsonmar/python-samples/blob/main/ml-metrics.py

STATUS: Partial working (confusion matrix error with random data) Classification Accuracy & Logarithmic Loss
"v001 new :ml-metrics.py"

This is an example of how to use PyTorch with Skikit to calculate performance metrics for Machine Learning.
Explained using PowerPoint available at https://7451111251303.gumroad.com/l/romzjt

Based on code at https://www.v7labs.com/blog/performance-metrics-in-machine-learning

Tested on macOS M2 14.5 (23F79) using Python 3.13.
flake8  E501 line too long, E222 multiple spaces after operator
"""
# STEP 1 = Setup. Before running this program: Installing Required Libraries & Importing Required Libraries
# brew install miniconda
# conda create -n py313
# conda activate py313
# conda install --name py313 numpy pytorch torchvision scikit-learn
# chmod +x ml-metrics.py
# ./ml-metrics.py

import numpy as np
import torch
from sklearn.metrics import roc_auc_score

# Built-in:
import argparse
import os
import datetime
import time


start_time = time.time()  # start the timer running.


# Globals:
DEBUGGING = False
SHOW_INPUTS = True
SHOW_STEPS = True
SHOW_PROGRESS = False
SHOW_ACCURACY = True
SHOW_INFO = True

GEN_RANDOM = True
TEST_SIZE_RATIO = 0.3

EPOCHS = 5
batch_size = 64
input_size = 28*28
hidden_size = 512
NUM_CLASSES = 10    # Number of classes in your classification task

PTH_MODEL_FILENAME="ml_with_pytorch_model.pth"  # output from this program.
REMOVE_FILE_AFTER_CREATION = True

learning_rate = 1e-3 # 0.001


def get_file_creation_time(file_path):
    """ Get the file's creation timestamp """
    creation_timestamp = os.path.getctime(file_path)

    # Convert the timestamp to a datetime object
    creation_date = datetime.datetime.fromtimestamp(creation_timestamp)

    # Format and return the creation date and time
    return creation_date.strftime("%Y-%m-%d %H:%M:%S")


def find_file_path(filename):
    cwd_path = os.path.join(os.getcwd(), filename)
    print(f"*** File found in current working directory: {cwd_path}")
    if os.path.exists(cwd_path):
        return f"*** File found in current working directory: {cwd_path}"

    ## Absolute Path Method
    abs_path = os.path.abspath(filename)
    if os.path.exists(abs_path):
        return f"*** File found with absolute path: {abs_path}"

    ## Search in Parent Directories
    current_dir = os.getcwd()
    print("os.getcwd()={current_dir}")
    while current_dir != os.path.dirname(current_dir):  # Stop at root directory
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path) is False:
            return f"*** INFO: File NOT found in parent directory: {file_path}"
        current_dir = os.path.dirname(current_dir)
    return file_path


def remove_file(file_path):
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Remove the file
            os.remove(file_path)
            #print(f"*** INFO: File removed from '{file_path}' ")
            return False
        else:
            print(f"*** ERROR: File '{file_path}' does not exist.")
            return True
    except PermissionError:
        print(f"*** ERROR: Permission denied. Unable to remove '{file_path}'.")
        return False
    except Exception as e:
        print(f"*** Exception occurred while trying to remove '{file_path}': {str(e)}")
        return False


def mean_absolute_error(y_true, y_pred):
    """ Calculate the absolute difference between actual and predicted values """
    abs_diff = torch.abs(y_true - y_pred)
    # Calculate the mean of the absolute differences
    mae = torch.mean(abs_diff)
    return mae


def mean_squared_error(y_true, y_pred):
   """ Calculate the squared difference between actual and predicted values """
   squared_diff = (y_true - y_pred) ** 2

   # Calculate the mean of the squared differences
   mse = torch.mean(squared_diff)
   return mse


def root_mean_squared_error(y_true, y_pred):
    """ Calculate the squared difference between actual and predicted values """
    squared_diff = (y_true - y_pred) ** 2
    # Calculate the mean of the squared differences
    mse = torch.mean(squared_diff)
    # Take the square root of the mean squared error to obtain RMSE
    rmse = torch.sqrt(mse)
    return rmse


def r_squared_error(y_true, y_pred):
    """ Calculate the mean of the actual values """
    y_mean = torch.mean(y_true)

    # Calculate the sum of squares (numerator)
    residual_sum_of_squares = torch.sum((y_true - y_pred) ** 2)

    # Calculate the total sum of squares (denominator)
    total_sum_of_squares = torch.sum((y_true - y_mean) ** 2)

    # Calculate R² using the formula
    r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares)

    return r_squared


def confusion_matrix(true_labels, pred_labels, num_classes):
    """
    Calculate the confusion matrix for a classification task.

    Args:
        true_labels (torch.Tensor): Ground truth labels.
        pred_labels (torch.Tensor): Predicted labels from the model.
        num_classes (int): Number of classes in the classification task.

    Returns:
        torch.Tensor: The confusion matrix of shape (num_classes, num_classes).
    """
    assert true_labels.shape == pred_labels.shape, "Shape mismatch between true_labels and pred_labels"
    cm = torch.zeros(num_classes, num_classes, dtype=torch.int64)

    for t, p in zip(true_labels.view(-1), pred_labels.view(-1)):
        cm[t.long(), p.long()] += 1

    return cm


def precision_recall(y_true, y_pred):
    assert y_true.shape == y_pred.shape, "Input tensors must have the same shape"

    # Convert predictions to binary (0 or 1) by applying a threshold (0.5 in this case)
    y_pred_binary = (y_pred >= 0.5).float()

    # Calculate True Positives (TP), False Positives (FP), and False Negatives (FN)
    TP = torch.sum(y_true * y_pred_binary)
    FP = torch.sum((1 - y_true) * y_pred_binary)
    FN = torch.sum(y_true * (1 - y_pred_binary))

    # Calculate Precision and Recall
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)

    return precision, recall


def f1_score(y_true, y_pred, eps=1e-8):
    assert y_true.size() == y_pred.size(), "Input tensors should have the same size"

    # Convert the predicted probabilities to binary predictions
    y_pred_binary = torch.round(y_pred)

    # Calculate True Positives, False Positives, and False Negatives
    tp = torch.sum(y_true * y_pred_binary)
    fp = torch.sum((1 - y_true) * y_pred_binary)
    fn = torch.sum(y_true * (1 - y_pred_binary))

    # Calculate Precision and Recall
    precision = tp / (tp + fp + eps)
    recall = tp / (tp + fn + eps)

    # Calculate F1 Score
    f1 = 2 * precision * recall / (precision + recall + eps)

    return f1.item()


# MAIN:

# Create tensors for actual and predicted values:
actual_values = torch.tensor([2.0, 4.0, 6.0, 8.0])
predicted_values = torch.tensor([2.5, 3.5, 6.5, 7.5])


# Calculate MAE
mae = mean_absolute_error(actual_values, predicted_values)
print(f"*** MAE (Mean Absolute Error)      : {mae:.4f}")

# Calculate MSE
mse = mean_squared_error(actual_values, predicted_values)
print(f"*** MSE (Mean Squared Error)       : {mse:.4f}")


# Calculate RMSE
rmse = root_mean_squared_error(actual_values, predicted_values)
print(f"*** RMSE (Root Mean Squared Error) : {rmse:.4f}")


# Calculate R²
r_squared = r_squared_error(actual_values, predicted_values)
print(f"*** RSE (R Squared Error)          : {r_squared:.4f}")


#if SHOW_STEPS:
#    print(f"*** Confusion Matrix:")
if SHOW_STEPS:
    print(f"*** Generating sample data randomly ...")
    true_labels = np.random.rand(100, 5)  # = X
    pred_labels = np.random.randint(0, 2, 100)
if DEBUGGING:
    print(f"true_lables={true_labels}")
    print(f"pred_lables={pred_labels}")

# cm = confusion_matrix(true_labels, pred_labels, NUM_CLASSES)
# print(f"cm={cm}")


# TODO: Classification Accuracy & Logarithmic Loss
# See https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234


# TODO: Calculate if imbalanced.
if SHOW_STEPS:
   print("*** STEP: For imbalanced datasets: Precision, Recall, and F1:")

# TODO: Choice of Randomness weighted toward TP, TN, etc.
y_true = torch.tensor([1, 0, 1, 1, 0, 1], dtype=torch.float32)
y_pred = torch.tensor([0.9, 0.3, 0.7, 0.1, 0.2, 0.8], dtype=torch.float32)
    # predicted probabilities for the positive class.

precision, recall = precision_recall(y_true, y_pred)
print(f"*** Precision   : {precision:.4f}")
print(f"*** Recall      : {recall:.4f}")

if SHOW_STEPS:
   print("*** STEP: harmonic mean of precision and recall for balance between FP & FN:")
f1 = f1_score(y_true, y_pred)
print(f"*** F1 Score    : {f1:.4f}")
    # A high F1 score indicates high precision (low false positives) and high recall (low false negatives),
    # which is desirable in some applications.


if SHOW_STEPS:
   print("*** STEP: Area Under the Receiver Operating Characteristic Curve:")
# Convert tensors to NumPy arrays, assuming you have the following PyTorch tensors:
y_true_np = y_true.detach().cpu().numpy()
    # a 1D tensor containing the true binary labels (0 or 1) for each sample
y_pred_np = y_pred.detach().cpu().numpy()
    # a 1D tensor containing the predicted probabilities for the positive class

auroc = roc_auc_score(y_true_np, y_pred_np)
    # True Positive Rate (TPR)=Recall / False Positive Rate (FPR)=(1 - Specificity)
print(f"*** AU-ROC score: {auroc:.4f}")
    # A higher AU-ROC value indicates better performance, with
    # a perfect classifier having an AU-ROC of 1 and
    # a random  classifier having an AU-ROC of 0.5.

exit()

# Create data loaders to iterate over data
train_dataloader = DataLoader(training_data, batch_size=batch_size)
train_dataloader_len = len(train_dataloader) * batch_size
test_dataloader = DataLoader(test_data, batch_size=batch_size)
test_dataloader_len = len(test_dataloader) * batch_size

if SHOW_INPUTS:
    print(f"*** learning_rate={learning_rate} ")
    print(f"*** Training data size:", train_dataloader_len )  # = 60032
    print(f"*** Test data size:", test_dataloader_len)  # = 10048
    for X, y in test_dataloader:
        print(f"*** Shape of X [N, C, H, W]: {X.shape}")
              # *** Shape of X [N, C, H, W]: torch.Size([64, 1, 28, 28])
        print(f"*** Shape of y: {y.shape} {y.dtype}")
              # *** Shape of y: torch.Size([64]) torch.int64
        break

# Ignore message: Failed to download (trying next): <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1000)>

# Determine the best device for performing training with cpu as the default device.
# Define the AI model as a neural network with 3 layers: an input layer, a hidden layer, and an output layer. Between the layers, we use a ReLU activation function.
# Since the input images are 1x28x28 tensors, we need to flatten the input tensors into a 784 element tensor using the Flatten module before passing the input into our neural network.

# Get device for training:
device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()  # TODO: Apple Silicon GPU
    else "cpu"  # CUDA not being used
)
if SHOW_INPUTS:
    print(f"*** Using device: {device} ")
        # Using cpu device

class NeuralNetwork(nn.Module):
    """ Define model """
    def __init__(self, input_size, hidden_size, NUM_CLASSES):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, NUM_CLASSES)
        )

    def forward(self, image_tensor):
        image_tensor = self.flatten(image_tensor)
        logits = self.linear_relu_stack(image_tensor)
        return logits


model = NeuralNetwork(input_size, hidden_size, num_classes).to(device)
if SHOW_INPUTS:
    print(f"*** model = {model}")
        # NeuralNetwork(
        #   (flatten): Flatten(start_dim=1, end_dim=-1)
        #   (linear_relu_stack): Sequential(
        #     (0): Linear(in_features=784, out_features=512, bias=True)
        #     (1): ReLU()
        #     (2): Linear(in_features=512, out_features=512, bias=True)
        #     (3): ReLU()
        #     (4): Linear(in_features=512, out_features=10, bias=True)
        #   )
        # )
        # DEFINITION: The ReLU (rectified linear unit) activation function introduces the
        # property of nonlinearity to a deep learning model and solves the "vanishing gradients" issue.
        # See https://builtin.com/machine-learning/relu-activation-function

# Define an AI model to recognize a hand written digit.
# Train the defined AI model using training data from the MNIST dataset.
# Test the trained AI model using testing data from the MNIST dataset.
# Evaluate

# STEP: Training Loop
   # Implement a training function to use with the train_dataloader to train our model.
   # Each iteration over the dataloader returns a batch_size image data tensor along with the expected output.
   # After moving the tensors to the device, we call the forward pass of our model,
   # compute the prediction error using the expected output and then
   # call the backwards pass to compute the gradients and apply them to the model parameters.


# Define our learning rate, loss function and optimizer:
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
if SHOW_INPUTS:
    print(f"*** loss_fn={loss_fn} ")
    print(f"*** optimizer={optimizer} ")
        # Adam (
        # Parameter Group 0
        #     amsgrad: False
        #     betas: (0.9, 0.999)
        #     capturable: False
        #     differentiable: False
        #     eps: 1e-08
        #     foreach: None
        #     fused: None
        #     lr: 0.001
        #     maximize: False
        #     weight_decay: 0
        # )

# Our training function:
def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()

    for batch_num, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Forward pass to compute prediction
        pred = model(X)
        # Compute prediction error using loss function
        loss = loss_fn(pred, y)

        # Backward pass
        optimizer.zero_grad() # zero any previous gradient calculations
        loss.backward() # calculate gradient
        optimizer.step() # update model parameters

        if batch_num > 0 and batch_num % 100 == 0:
            loss, current = loss.item(), batch_num * len(X)
            if SHOW_PROGRESS:
                print(f"*** loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    for X, y in dataloader:
        X, y = X.to(device), y.to(device)
        pred = model(X)
        test_loss += loss_fn(pred, y).item()
        correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    if SHOW_PROGRESS:
        print(f"*** Test Error: Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f}")


# STEP: Train the model for 5 epochs over the dataset:
if SHOW_STEPS:
    print(f"*** STEP: Training the model for {EPOCHS} epochs over the dataset:")
for t in range(EPOCHS):
    if SHOW_STEPS:
        print(f"*** STEP: Epoch {t+1}...")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)


# STEP: Save our trained model parameters for inferencing (making predictions):
torch.save(model.state_dict(), PTH_MODEL_FILENAME)
if SHOW_INFO:
    PTH_MODEL_FILEPATH = os.path.join(os.getcwd(), PTH_MODEL_FILENAME)
    creation_time = get_file_creation_time(PTH_MODEL_FILEPATH)
    print(f"*** INFO: PyTorch Model State saved to file path: {PTH_MODEL_FILEPATH} at {creation_time}.")

# Load the saved model parameters into a new instance of the model
model = NeuralNetwork(input_size, hidden_size, NUM_CLASSES).to(device)
model.load_state_dict(torch.load(PTH_MODEL_FILENAME))

if SHOW_STEPS:
    print(f"*** STEP: Inference using the new model instance...")
model.eval()
for i in range(10):
    x, y = test_data[i][0], test_data[i][1]
    x = x.to(device)
    pred = model(x)
    predicted, actual = pred[0].argmax(0).item(), y
    print(f'*** Predicted: "{predicted}", Actual: "{actual}"')
        # Predicted: "7", Actual: "7"


# TODO: STEP: Calculate summary Confusion & Evaluation Metrics
# See https://www.v7labs.com/blog/performance-metrics-in-machine-learning
# (F measure accuracy, error True/False Positive/Negative, precision, recall
# Cross-validation helps check performance across different data subsets. AUC-ROC curves are handy for binary classification.
# while MSE and RMSE quantify error magnitude, R-squared gives a sense of the model's explanatory power.
# mean average precision (MAP), and normalized discounted cumulative gain


# STEP: Calculate the execution time
end_time = time.time()
execution_time = end_time - start_time
# PROTIP: Output run time with input for correlation:
print(f"*** LOG: Program took {execution_time:.4f} seconds for {device} to run {EPOCHS} epochs on {NUM_CLASSES} classes with {test_dataloader_len} / {train_dataloader_len} items within {batch_size} batches.")
      # TODO: Add out_features


# STEP: Remove files downloaded:
if REMOVE_FILE_AFTER_CREATION:
    if remove_file(PTH_MODEL_FILEPATH):
        if SHOW_INFO:
            print(f"*** INFO: File removed from '{PTH_MODEL_FILEPATH}' ")

"""
*** MAE (Mean Absolute Error)      : 0.5000
*** MSE (Mean Squared Error)       : 0.2500
*** RMSE (Root Mean Squared Error) : 0.5000
*** RSE (R Squared Error)          : 0.9500
*** Generating sample data randomly ...
*** STEP: For imbalanced datasets: Precision, Recall, and F1:
*** Precision   : 1.0000
*** Recall      : 0.7500
*** STEP: harmonic mean of precision and recall for balance between FP & FN:
*** F1 Score    : 0.8571
*** STEP: Area Under the Receiver Operating Characteristic Curve:
*** AU-ROC score: 0.7500
"""
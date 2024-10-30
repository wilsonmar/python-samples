#!/usr/bin/env python3

""" pytorch-mnist.py at https://github.com/wilsonmar/python-samples/blob/main/pytorch-mnist.py
STATUS: Being built
"v001 new :pytorch-mnist.py"
Tested on macOS M2 14.5 (23F79) using Python 3.13.
flake8  E501 line too long, E222 multiple spaces after operator

This is an example of how to use PyTorch to load the legacy MNIST database of hand-written digits.
* https://en.wikipedia.org/wiki/MNIST_database

Code here is based on IBM Developer course "Getting Started with Machine Learning with PyTorch" (dated 2023-05-01)
at https://cognitiveclass.ai/courses/getting-started-with-machine-learning-with-pytorch
which creates a Jupyter environment
at https://labs.cognitiveclass.ai/v2/tools/jupyterlab?ulid=ulid-af6b90d695505216e5ab9d00b67cc8bd64b4bbc6

"""
# STEP 1 = Setup. Before running this program: Installing Required Libraries & Importing Required Libraries
# brew install miniconda
# conda create -n py313
# conda activate py313
# conda install --name py313 pytorch torchvision scikit-learn
# install
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

# Built-in:
import argparse
import os
import datetime
import time


start_time = time.time()


# Globals:
SHOW_INPUTS = True
SHOW_STEPS = True
SHOW_PROGRESS = False
SHOW_ACCURACY = True
SHOW_INFO = True
DEBUGGING = False

PTH_MODEL_FILENAME="ml_with_pytorch_model.pth"  # output from this program.
REMOVE_FILE_AFTER_CREATION = True

EPOCHS = 5
input_size = 28*28
hidden_size = 512
num_classes = 10
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


# STEP: Download the MNIST dataset and create a DataLoader for the dataset.
# Download training data from MNIST datasets containing 28x28 pixel images of digits 0 through 9.
training_data = datasets.MNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)
# Download test data from open datasets.
test_data = datasets.MNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

batch_size = 64

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

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
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
model = NeuralNetwork(input_size, hidden_size, num_classes).to(device)
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
print(f"*** LOG: Program took {execution_time:.4f} seconds for {device} to run {EPOCHS} epochs on {num_classes} classes with {test_dataloader_len} / {train_dataloader_len} items within {batch_size} batches.")
      # TODO: Add out_features


# STEP: Remove files downloaded:
if REMOVE_FILE_AFTER_CREATION:
    if remove_file(PTH_MODEL_FILEPATH):
        if SHOW_INFO:
            print(f"*** INFO: File removed from '{PTH_MODEL_FILEPATH}' ")

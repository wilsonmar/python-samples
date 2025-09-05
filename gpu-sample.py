#!/usr/bin/env python3

"""gpu-sample.py here.

This code runs PyTorch on macs v12.3+ with Silicon (preferabbly M1/M2 chips) and
Apple's MPS (Metal Performance Shaders) backend to PyTorch and tensorflow-metal plugin provided by Apple.
PyTorch v1.12+ for Mac (Silicon) was announced May 18, 2022 https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac
See https://wiki.cci.arts.ac.uk/books/how-to-guides/page/enable-gpu-support-with-pytorch-macos
MPS is instead of CUDA: NVIDIA's proprietary GPU computing platform designed for NVIDIA GPUs not available on Macs.
https://www.youtube.com/watch?v=CbmTFTsbyPI

# Here are sample code to detect and use GPU on macOS and Google Colab.
# PyTorch is open-sourced by Meta (FaceBook). "An open source deep learning platform that provides a seamless path from research prototyping to production deployment."
# See https://www.laurencegellert.com/2023/10/how-make-python-code-run-on-the-gpu/

# TODO: Update versions:
# from https://www.youtube.com/watch?v=uYas6ysyjgY GPU-Acceleration PyTorch on M1 Macs!
#  and https://www.youtube.com/watch?v=VEDy-c5Sk8Y
# Based on https://www.youtube.com/watch?v=Zx2MHdRgAIc Setup for Machine Learning with PyTorch
# https://github.com/mrdbourke/pytorch-apple-silicon

# Before running, on a Terminal:
     CONDA_SUBDIR=osx_-arm64 conda create -n ml python=3.9 -c conda-forge
     conda activate ml
     conda env config vars set CONDA_SUBDIR=osx-arm64
     curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

     To view your CPU and GPU usage, Open Activity Monitor, then Window -> GPU History (command 4), and then Window -> CPU History (command 3).

     uv run gpu-sample.py
"""
__last_change__ = "25-09-05 v003 + mps & cpu support :gpu-sample.py"

import numpy as np          # uv pip install numpy
import re
import subprocess
import torch                # uv pip install torch torchvision torchaudio
    #    uv pip install torch
    #       The PyTorch library has been successfully installed! Here's what was installed:
    #       •  torch==2.8.0 - The main PyTorch framework
    #       •  filelock==3.19.1 - File locking utilities
    #       •  fsspec==2025.9.0 - Filesystem specification
    #       •  jinja2==3.1.6 - Template engine
    #       •  mpmath==1.3.0 - Multi-precision arithmetic library
    #       •  networkx==3.5 - Network analysis library
    #       •  sympy==1.14.0 - Symbolic mathematics library
    # TorchServe is designed specifically for serving and scaling PyTorch models in production environments. 
    # It supports REST APIs for model inference, batching, versioning, and monitoring.
    # TorchRecipes = https://github.com/facebookresearch/recipes
    # TorchScript to convert models into a form that can be optimized and run independently of Python.
# from numba import cuda    # uv pip install cuda
import tensorflow as tf   # uv pip install tensorflow-macos tensorflow-metal
#from transformers import AutoTokenizer, AutoModel   # uv pip install transformers
#from datasets import load_dataset                   # uv pip install datasets

# uv pip install tensorflow-metal  # TensorFlow with Metal support

print(f"Numpy version: {np.__version__}")   # 1.26.4
print(f"Torch version: {torch.__version__}")   # 1.26.4
print(f"Tensorflow version: {tf.__version__}")   # 1.26.4

# TODO: Additional sample code from:
# https://github.com/pytorch/examples
# https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/
# https://github.com/ageron/handson-mlp = Hugging Face libraries to download datasets and pretrained models, including transformer models. Transformers are incredibly powerful and versatile, and they are the main building block of virtually all AI assistants today. 

# Intel x86 Macs can't use GPU acceleration because they don't have CUDA support like Apple Silicon Macs.



def apple_silicon_chip() -> str | None:
    """Return True if machine has Apple Silicon chip (M1-M4, etc.).

    This approach avoids false negatives under "arm" platform emulation and 
    thus more robust for real chip detection.
    """
    #import subprocess
    #import re
    try:
        cmd = ['system_profiler', 'SPHardwareDataType']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
        if result.returncode != 0:
            return None
        match = re.search(r'Chip: Apple (M\d+)', result.stdout)
        return match.group(1) if match else None
    except Exception:
        return None

# If a CUDA is available, use it:
use_cuda = torch.cuda.is_available()
print("\nCUDA GPU Available:", use_cuda)   # False on macOS.
if use_cuda:
    print("CUDA Version:", torch.version.cuda)
    print("Number of GPUs:", torch.cuda.device_count())
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("GPU Memory (GB):", torch.cuda.get_device_properties(0).total_memory / 1e9)

    # import tensorflow as tf
    print("TensorFlow Version:", tf.__version__)
    print("GPUs Available:", len(tf.config.list_physical_devices('GPU')))

    # uv pip install nvidia-ml-py3  # For NVIDIA GPU monitoring
else:
    chip = apple_silicon_chip()   # chip="M1" or "M2", etc. or None
    if not chip:   # None
        device = torch.device("cpu")  # Intel Mac or Raspberry Pi
        print(f"WARNING: Using device \"{device}\"" )
    else:
        device = torch.device("mps")  # Use Apple Silicon (Metal Performance Shaders) GPUs
        print(f"VERBOSE: Using device \"{device}\" on Apple Silicon \"{chip}\" chip.")

        if torch.backends.mps.is_built():   # bool
            print("VERBOSE: backends.mps.is_built() = True")
        else:
            print("FATAL: backends.mps.is_built() = False")
            exit() # stop running.

        if torch.backends.mps.is_available():  # torch.has_mps
            mps_device = torch.device("mps")
            x = torch.ones(1, device=mps_device)
            device = torch.device("mps")  # Use Apple Silicon GPU
            print(x)  # tensor([1.], device='mps:0')


### Tasks by a GPU:

# Programming in TensorFlow (and GPU libraries in general) requires thinking a bit differently vs conventional “procedural logic”. Instead of working on one unit at a time, TensorFlow works on all elements at once. Lists of data need to be kept in special Tensor objects (which accept numpy arrays as inputs). Operations like add, subtract, and multiply are overloaded on Tensors. Behind the scenes when you add/subtract/multiply Tensors it breaks up the data into smaller chunks and the work is farmed out to the GPUs in parallel. There is overhead to do this though, and the CPU bears the brunt of that. If your data set is small, the GPU approach will actually run slower. As the data set grows the GPU will eventually prove to be much more efficient and make tasks possible that were previously unfeasible with CPU only.

# summarizing values in an array (map / reduce)
# matrix multiplication, array operations
# image processing (images are arrays of pixels)
# machine learning which uses a combination of the above.

# Move models/tensors to that device:
#model.to(device)
#tensor = tensor.to(device)

# Example: allocate:
x = torch.ones(5, device=device)
# Model example
#model = YourModelClass().to(device)
#y = model(x)

# Any model.to(device) and tensor to(device) calls work exactly the same with "mps" as with "cuda".
print(f"\nTASK 1: x+y=z tensor operation on GPU device: \"{device}\" ")
x = torch.tensor([1.0, 2.0, 3.0], device=device)
y = torch.tensor([4.0, 5.0, 6.0], device=device)
z = x + y
print(f"x={x}")
print(f"y={y}")
print(f"z={z}")

# https://www.youtube.com/watch?v=53PjsHUd46E&t=8m32s On a recent MacBook (M1/M2/M3), MPS will be notably faster than CPU but still around half the speed of an equivalent Nvidia GPU for most vision models.
#[01:24 Train Predict Checkpoint https://github.com/milesial/Pytorch-Unet image semantic segmentation with high quality images in #U-Net Semantic Segmentation repo https://github.com/milesial/Pytorch-UNet
  
#[06:07 Casting Data types to .float32
#U-Net Classifier-Free Diffusion Guidance paper https://arxiv.org/pdf/2207.12598 

#[09:27 Add "to(device)." so all runs on device using CLIP model for Image Encodings.
# clip_img_encoding = clip_model.to(device).encode_image(clip_imgs)


# https://www.youtube.com/watch?v=0wxobKsnf2o Apple M3Max MLX beats RTX4090m!

# Apple MPS often benefits from smaller batch sizes due to unified memory architecture:
# On MPS, use batch_size=16 or batch_size=8 instead of typical CUDA sizes.

# Replace torch.cuda.set_device or CUDA-only APIs with generic torch.device.


# print(f"\nTASK 2: Mandelbrot Set fractal on GPU device: {device}")
# To compare the performance on a MacBook Pro’s CPU vs GPU, run 
# the https://en.wikipedia.org/wiki/Mandelbrot_set
# https://realpython.com/mandelbrot-set-python/ – complete tutorial on drawing the Mandelbrot set in Python, including colorization, and zooming into the spiral arms.
# https://dzone.com/articles/mandelbrot-set-in-tensorflow – an example using TensorFlow.
# Notice GPU significantly exceeds GPU only at higher (15000x15000)

def tensor_flow_step(self, c_vals_, z_vals_, divergence_scores_):
    """Process compute_mandelbrot_tensor_flow() to compute all pixels in parallel.

    :param c_vals_: array of complex values for each coordinate
    :param z_vals_: z value of each coordinate, starts at 0 and is recomputed each step
    :param divergence_scores_: the number of iterations taken before divergence for each pixel
    :return: the updated inputs
    """
    z_vals_ = z_vals_*z_vals_ + c_vals_

    # find z-values that have not diverged, and increment those elements only
    not_diverged = tf.abs(z_vals_) < 4
    divergence_scores_ = tf.add(divergence_scores_, tf.cast(not_diverged, tf.float32))

    return c_vals_, z_vals_, divergence_scores_

def compute(self, device='/GPU:0'):
    """Compute the mandelbrot set using TensorFlow.

    :return: array of pixels, value is divergence score 0 - 255
    """
    with tf.device(device):

        # build x and y grids
        y_grid, x_grid = np.mgrid[self.Y_START:self.Y_END:self.Y_STEP, self.X_START:self.X_END:self.X_STEP]

        # compute all the constants for each pixel, and load into a tensor
        pixel_constants = x_grid + 1j*y_grid
        c_vals = tf.constant(pixel_constants.astype(np.complex64))

        # setup a tensor grid of pixel values initialized at zero
        # this will get loaded with the divergence score for each pixel
        z_vals = tf.zeros_like(c_vals)

        # store the number of iterations taken before divergence for each pixel
        divergence_scores = tf.Variable(tf.zeros_like(c_vals, tf.float32))

        # process each pixel simultaneously using tensor flow
        for n in range(self.MANDELBROT_MAX_ITERATIONS):
            c_vals, z_vals, divergence_scores = self.tensor_flow_step(c_vals, z_vals, divergence_scores)
            self.console_progress(n, self.MANDELBROT_MAX_ITERATIONS - 1)

        # normalize score values to a 0 - 255 value
        pixels_tf = np.array(divergence_scores)
        pixels_tf = 255 * pixels_tf / self.MANDELBROT_MAX_ITERATIONS

        return pixels_tf
    
# compute(self)

# Using with BERT
        # https://www.youtube.com/watch?v=uYas6ysyjgY GPU-Acceleration for PyTorch on M1 Macs!
        # https://www.youtube.com/watch?v=-TOdEjcFldI


# For custom GPU operations in Python, use pyobjc to interface with Apple Metal APIs, but it is more complex than using PyTorch/TensorFlow.

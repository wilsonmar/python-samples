#!/usr/bin/env python3

"""gpu-sample.py here.

https://github.com/wilsonmar/python-samples/blob/main/gpu-sample.py

This code provides a microbenchmark structure to compare results of several runs of 
PyTorch displayed as a bar graph such as this:
https://res.cloudinary.com/dcajqrroq/image/upload/v1757128591/mac-mps-1033x626_w6wx1p.png

The comparison of run speeds for reproducing Artificial Neural Network (ANN) "deep learning" training and evaluation of various datasets using set batch sizes: 
   * ResNet50 (Residual Network Learning for Image Recognition) for computer vision https://viso.ai/deep-learning/resnet-residual-neural-network/
   * HuggingFace BERT (batch size 64) https://viso.ai/deep-learning/vgg-very-deep-convolutional-networks/
   * VGG 19 (batch size 64)
   * AlexNet https://viso.ai/deep-learning/alexnet/
   * MobileNet
   * Datasets MNIST - see pytorch-mnist.py in wilsonmar/python-samples
   * CIFAR
   * https://viso.ai/deep-learning/yolov7-guide/
   * others imported using ONNX (Open Neural Network Exchange) format and tools.
https://viso.ai/deep-learning/pytorch-vs-tensorflow/

For hardware-assisted parallel asynchronous execution of collective operations and peer-to-peer communication, in addition to "cuda" devices (from NVIDIA), PyTorch now supports "mps" devices, named for Apple's Metal Performance Shaders backend to PyTorch through a  tensorflow-metal plugin provided by Apple. Device "cpu" means no GPU acceleration is used. QUESTION: Raspberry Pi AI chip?

Additional comparisons planned are of https://viso.ai/computer-vision/opencv/ 
torchvision torchaudio

Open-sourced by Meta (FaceBook) in 2016, PyTorch v1.12+ was announced May 18, 2022 with for MacOS on Apple Silicon M1/M2/M3/M4 chips which have GPU capabilities. 

Previous to that, PyTorch supported only CUDA devices. NVIDIA's proprietary GPU computing platform designed for NVIDIA GPUs not available on Macs. After macOS High Sierra, Apple dropped system-level support of external GPU drivers with AMD Radeon Pro 580 cards connected through Thunderbolt 3/4 (not USB) cables to eGPU enclosures on Intel Macs. See https://support.apple.com/en-us/102363


# References:
------------
   * https://www.laurencegellert.com/2023/10/how-make-python-code-run-on-the-gpu/
   * https://pytorch.org/blog/introducing-accelerated-pytorch-training-on-mac
   * https://wiki.cci.arts.ac.uk/books/how-to-guides/page/enable-gpu-support-with-pytorch-macos
   * https://www.youtube.com/watch?v=CbmTFTsbyPI

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

     uv venv venv
     source .venv/bin/activate
     uv venv --python python3.12
     uv add psutil numpy torch torchvision torchaudio tensorflow source subprocess-v
     chmod +x gpu-sample.py
     uv pip install requests
     ruff check gpu-sample.py
     uv run gpu-sample.py
"""
__last_change__ = "25-09-10 v005 + subprocess-tee :gpu-sample.py"

# Built-in libraries:
import argparse
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import NamedTuple

# External libraries defined in requirements.txt:
try:
    #import matplotlib. pyplot
    import numpy as np          # uv pip install numpy
    import platform
    import psutil
    import re
    import subprocess_tee    # uv add subprocess-tee
    # from subprocess_tee import run    # uv add subprocess-tee
    # [B404:blacklist] Consider possible security implications associated with the subprocess module.
    import torch        # uv pip install torch torchvision torchaudio
    from torch import Tensor
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
        # TorchScript to convert models to be optimized and run independently of Python.
    import torchvision  # https://download.pytorch.org/whl/cu%7BCUDA_VERSION%7D/torch_stable.html
    from torchvision import transforms
    import torchaudio 
    # audio backends to load/save audio data (ffmpeg, sox, or soundfile) 
    # import sounddevice   # uv pip install sounddevice  # also: tqdm. # deprecated?

    # from numba import cuda    # uv pip install cuda
    import tensorflow as tf   # uv pip install tensorflow-macos tensorflow-metal
    #from transformers import AutoTokenizer, AutoModel   # uv pip install transformers
    #from datasets import load_dataset                   # uv pip install datasets
except Exception as e:
    print(f"Python module import failed: {e}")
    # uv run log-time-csv.py
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:\n  uv env env\n  source .venv/bin/activate")
    exit(9)

# uv pip install tensorflow-metal  # TensorFlow with Metal support


# Global static variables:
SHOW_VERBOSE = False
SHOW_DEBUG = False
SHOW_SUMMARY = False
MAX_LOOPS = 3   # 0 = infinite
SLEEP_SECS = 1

# Program Timings:
# For wall time measurements:
pgm_strt_datetimestamp = datetime.now()


def read_cmd_args() -> None:
    """Read command line arguments and set global variables.

    See https://realpython.com/command-line-interfaces-python-argparse/
    """
    #import argparse
    #from argparse import ArgumentParser
    parser = argparse.ArgumentParser(allow_abbrev=True,description="swap-a-secret.py")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run without output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show inputs into functions")
    parser.add_argument("-vv", "--debug", action="store_true", help="Debug outputs from functions")
    parser.add_argument("-s", "--summary", action="store_true", help="Show summary stats")
    # Default -h = --help (list arguments)
    args = parser.parse_args()


    #### SECTION 08 - Override defaults and .env file with run-time parms:

    # In sequence of workflow:

    global SHOW_VERBOSE, SHOW_DEBUG, SHOW_SUMMARY
    if args.verbose:       # -v  --verbose
        SHOW_VERBOSE = True
    if args.debug:         # -vv --debug
        SHOW_DEBUG = True
    if args.summary:       # -s  --summary
        SHOW_SUMMARY = True

    if args.quiet:         # -q --quiet
        SHOW_VERBOSE = False
        SHOW_DEBUG = False
        SHOW_SUMMARY = False

    return None


### OS-level utilities:

def is_macos() -> bool:
    """Return True if this is running on macOS."""
    # import platform
    return platform.system() == "Darwin"

def apple_silicon_chip() -> str | None:
    """Return True if machine has Apple Silicon chip (M1-M4, etc.).

    This approach avoids false negatives under "arm" platform emulation and 
    thus more robust for real chip detection.
    """
    #import subprocess-tee
    #import re
    try:
        cmd = ['system_profiler', 'SPHardwareDataType']
        # Substitute subprocess module flagged by bandit:
        result = subprocess_tee.run(cmd, stdout=subprocess_tee.PIPE, stderr=subprocess_tee.PIPE, encoding='utf8')
        if result.returncode != 0:
            return None
        match = re.search(r'Chip: Apple (M\d+)', result.stdout)
        return match.group(1) if match else None
    except Exception:
        return None

def cuda_env_display():
    """Display environment stats when CUDA is available for use."""
    print("CUDA Version:", torch.version.cuda)
    print("Number of GPUs:", torch.cuda.device_count())
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("GPU Memory (GB):", torch.cuda.get_device_properties(0).total_memory / 1e9)

    # import tensorflow as tf
    print("TensorFlow Version:", tf.__version__)
    print("GPUs Available:", len(tf.config.list_physical_devices('GPU')))

    print(f"Numpy version: {np.__version__}")   # 1.26.4

    # uv pip install nvidia-ml-py3  # For NVIDIA GPU monitoring

def chip_device_to_use() -> str:
    """Determine GPU device to use ("cuda", "mps", "cpu").
    
    For cross-platform use of PyTorch with or without CUDA.
    """
    if SHOW_VERBOSE:
        print(f"VERBOSE: Torch version: {torch.__version__}")   # 1.26.4
    # If a CUDA is available, use it:
    use_cuda = torch.cuda.is_available()
    if use_cuda:
        device = torch.device("cuda")
        if SHOW_VERBOSE:
            print(f"VERBOSE: device \"{device}\" available.")
        cuda_env_display()
        return device

    if not is_macos:  # Linux Raspberry Pi?
        device = torch.device("cpu")
        print(f"WARNING: Neither CUDA nor MPS available. Using \"{device}\"." )
        return device

    # Intel x86 Macs can't use GPU acceleration because they don't have CUDA support like Apple Silicon Macs.
    chip = apple_silicon_chip()   # chip="M1" or "M2", etc. or None
    if not chip:   # None -> fallback to use CPU:
        device = torch.device("cpu")  # Intel Mac
        print(f"WARNING: Neither CUDA nor MPS available. Using \"{device}\"." )
        return device
    
    if not torch.backends.mps.is_built():
        device = torch.device("cpu")
        print("WARNING: backends.mps.is_built() = False, so fallback to cpu")
        return device

    if not torch.backends.mps.is_available():  # torch.has_mps
        print("ERROR: backends.mps.is_built() = True but not available.")
        device = torch.device("cpu")
        return device

    device = torch.device("mps")  # Use Metal Performance Shaders GPUs
    if SHOW_VERBOSE:
        print(f"VERBOSE: device \"{device}\" available on Apple Silicon \"{chip}\" chip.")
    return device

# For custom GPU operations in Python, use pyobjc to interface with Apple Metal APIs, but it is more complex than using PyTorch/TensorFlow.


#### Utility Functions:

def gen_local_timestamp() -> str:
    """Generate a timestamp straing containing the local time with AM/PM & Time zone code."""
    # import pytz
    # now = datetime.now(tz)  # adds time zone.

    # from datetime import datetime
    local_time_obj = datetime.now().astimezone()
    local_timestamp = local_time_obj.strftime("%Y-%m-%d_%I:%M:%S %p %Z%z")  # local timestamp with AM/PM & Time zone codes
    return local_timestamp

def gen_utc_timestamp() -> str:
    """Generate a timestamp straing containing the UTC "Z" time with no AM/PM & Time zone code."""
    # import time
    timestamp = time.time()   # UTC epoch time.
    # from datetime import datetime, timezone
    # Get the current UTC time as a timezone-aware datetime object
    now_utc = datetime.now(timezone.utc)
    # Format the UTC timestamp as a string, e.g., ISO 8601 format
    timestamp = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    return timestamp

def func_timer_strt():
    """Capture start time for elapsed seconds calculation by func_timer_stop()."""
    strt_func_time = time.perf_counter()
    return strt_func_time
    
def func_timer_stop(strt_time):
    """Calculate elapsed seconds using start time previously captured."""
    stop_time = time.perf_counter()
    elapsed_secs = stop_time - strt_time
    return elapsed_secs


def user_gb_mem_avail() -> float:
    """Return the GB of RAM for system, using the psutil library.
    
    cross-platform vs. /proc/meminfo Linux sums "MemFree", "Buffers", and "Cached" values in kB.
    """
    #import os, psutil  #  psutil-5.9.5
    memory_bytes = psutil.virtual_memory().available  # for user
    gb = memory_bytes / (1024 ** 3)  # from bytes to Gb
    return gb

def pgm_memory_used() -> (float, str):
    """Return the MiB of RAM for the current process, using the psutil library."""
    #import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    process_info = str(process)
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    return mem, process_info

def pgm_diskspace_free() -> float:
    """Return the GB of disk space free of the partition in use, using the psutil library."""
    #import os, psutil  #  psutil-5.9.5
    disk = psutil.disk_usage('/')
    free_space_gb = disk.free / (1024 * 1024 * 1024)  # = 1024 * 1024 * 1024
    return free_space_gb


def pgm_summary(std_strt_datetimestamp, loops_count):
    """Print summary count of files processed and the time to do them."""
    # For wall time of standard imports:
    pgm_stop_datetimestamp = datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp - pgm_strt_datetimestamp

    if SHOW_DEBUG:
        pgm_stop_mem_used, process_data = pgm_memory_used()
        pgm_stop_mem_diff = pgm_stop_mem_used - pgm_strt_mem_used
        print(f"{pgm_stop_mem_diff:.6f} MB memory consumed during run in {process_data}.")

        pgm_stop_disk_diff = pgm_strt_disk_free - pgm_diskspace_free()
        print(f"{pgm_stop_disk_diff:.6f} GB disk space consumed during run.")

        print(f"SUMMARY: Ended while attempting loop {loops_count} in {pgm_elapsed_wall_time} seconds.")
    else:
        print(f"SUMMARY: Ended while attempting loop {loops_count}.")


## PyTorch functions:

def sound_from_torchaudio() -> str:
    """Return speech command from built-in torchaudio speech dataset.
    
    The SPEECHCOMMANDS class was first created by Pete Warden at Google and released as part of the TensorFlow Speech Recognition Challenge meant for training and testing machine learning models in speech recognition tasks (to build and evaluate voice-controlled tools, speech recognition systems, and audio processing algorithms). Initially, a 2.4 GB .tar.gz archive had over 105,000 one-second audio clips spoken by a wide range of people. There are several .wav files for each of 35 short words:
        # DIRECTION: backward, down, follow, forward, go, left, right, stop, up
        # NAMES: marvin, sheila, no, off, on, visual, yes
        # OBJECTS: bed, house, learn, tree
        # ANIMALS: bird, cat, dog
        # NUMBERS: eight, five, four, nine, one, seven, six, three, two, zero
        # EMOTIONS: happy, wow
    """
    from torchaudio.datasets import SPEECHCOMMANDS
    print("WARNING: folder SpeechCommands/speech_commands_v0.02 created under pwd is 2.3GB!")
    # from typing import NamedTuple
    # from torch import Tensor
    # TODO: The decoding and encoding capabilities of PyTorch for both audio and video are being consolidated into TorchCodec. Please see https://github.com/pytorch/audio/issues/3902
        
    # import soundfile
    print(f"{torchaudio.list_audio_backends()}")
    # FIXME: UserWarning: torchaudio._backend.list_audio_backends has been deprecated. This deprecation is part of a large refactoring effort to transition TorchAudio into a maintenance phase. The decoding and encoding capabilities of PyTorch for both audio and video are being consolidated into TorchCodec. Please see https://github.com/pytorch/audio/issues/3902 for more information. It will be removed from the 2.9 release. 
    exit()
    class SpeechSample(NamedTuple):
        waveform: Tensor   # path
        sample_rate: int
        label: str
        speaker_id: str
        utterance_number: int
    # FIXME: port your code to rely directly on TorchCodec's decoder instead: https://docs.pytorch.org/torchcodec/stable/generated/torchcodec.decoders.AudioDecoder.html#torchcodec.decoders.AudioDecoder.
    # afplay /Users/johndoe/github-wilsonmar/python-samples/SpeechCommands/speech_commands_v0.02/backward/02ade946_nohash_4.wav
    try:
        speech_commands_dataset = SPEECHCOMMANDS(root=Path.cwd(), download=True)
        #speech_commands_dataset = SPEECHCOMMANDS(root=".", download=True)

        # speech_sample = SpeechSample(*speech_commands_dataset[1])
        # FIXME: ERROR: Speech_command_dataset download: Couldn't find appropriate backend to handle uri /Users/johndoe/github-wilsonmar/python-samples/SpeechCommands/speech_commands_v0.02/backward/02ade946_nohash_4.wav and format None.
        speech_sample = "/Users/johndoe/github-wilsonmar/python-samples/SpeechCommands/speech_commands_v0.02/backward/02ade946_nohash_4.wav"
        speech_sample
        exit()
        # print(f"DEBUG: speech_command_dataset[10]={speech_command_dataset.get_metadata(10)} ")
    except Exception as e:
        print(f"ERROR: Speech_command_dataset download: {e}")
        return None  # TODO: Generate one instead?

    waveform, sample_rate, label, speaker_id, utterance_num = speech_commands_dataset[10]
        # waveform: Tensor
        # sample_rate: int
        # label: str
        # speaker_id: str
        # utterance_number: int

    # A waveform is the visual representation of sound pressure amplitude (loudness) as it travels through air over a duration of time:
    # Frequency is how many times a sound wave repeats itself in one second. 440 Hz (A4 note) is the international standard pitch reference for tuning instruments.
    # The human ear can hear frequencies up to around 20,000 Hz, which is why audio formats like CDs use a 44,100 Hz sampling rate to accurately capture the full range of human hearing.
    print(label)  # Returns speech command, like 'backward'

    # Trend the highest levels of memory allocation and caching on the GPU,
    # to identify trends for identifying memory leaks or inefficiencies:
    # torch.cuda.max_memory_allocated()
    # torch.cuda.max_memory_cached()
    
    # Release GPU memory no longer in use:
    # torch.cuda.empty_cache() 

    return label


def wav_shape_rate_torchaudio(filepath="audio/sample-1mb.wav") -> (str, float):
    """Use torchaudio to id waveform shape and sample rate of a .wav file."""
    # from https://file-examples.com/index.php/sample-audio-files/sample-wav-download/
    #import torchaudio
    #from torchaudio import transforms
    if SHOW_VERBOSE:
        print(f"VERBOSE: torchaudio.__version__ = {torchaudio.__version__} {torchaudio.__version__} ")
    # https://github.com/pytorch/audio/issues/3902 
        # print(f"VERBOSE: torchaudio.list_audio_backends() = {torchaudio.list_audio_backends()} ")
    
    return None, None

    # Check waveform shape and sample rate:
    waveform, sample_rate = torchaudio.load(filepath)
    if SHOW_VERBOSE:
        print(f"VERBOSE: waveform.shape={waveform.shape}, sample_rate={sample_rate} ")
    return waveform.shape, sample_rate

def numpy_to_torchaudio(speed=16000) -> str:
    """Convert random numpy array (from streaming mic) into tensors."""
    # See https://realpython.com/python-torchaudio/

    # FIXME: UserWarning: In 2.9, this function's implementation will be changed to use torchaudio.load_with_torchcodec` under the hood. Some parameters like ``normalize``, ``format``, ``buffer_size``, and ``backend`` will be ignored. We recommend that you port your code to rely directly on TorchCodec's decoder instead: https://docs.pytorch.org/torchcodec/stable/generated/torchcodec.decoders.AudioDecoder.html#torchcodec.decoders.AudioDecoder.

    #import torch
    #import numpy as np
    # TODO: Substitute a live numpy array instead of random:
    mic_array = np.random.randn(int(speed))  # Simulated 1 sec of mono audio
    waveform = torch.tensor(mic_array)
    return waveform

def normalize_color_torchvision(filepath="./imagenet"):
    """Use PyTorch TorchVision library to convert images to tensors, normalize color."""
    # Maintained by Francisco Massa https://www.youtube.com/watch?v=CU6bTEClzlw
    # See https://www.clouddefense.ai/code/python/example/torchvision
    # https://www.youtube.com/watch?v=Zvd276j9sZ8
    #import torchvision
    # from torchvision import transforms

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406),
                            std=(0.229, 0.224, 0.225)),
    ])
    
    # Load ImageNet dataset (replace with actual path):
    train_dataset = torchvision.datasets.ImageNet(
        root=filepath, split="train", transform=transform
    )

    # Load images using DataLoader:
    from torch.utils.data import DataLoader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    return train_loader


### PyTorch

# Programming in TensorFlow (and GPU libraries in general) requires thinking a bit differently vs conventional “procedural logic”. Instead of working on one unit at a time, TensorFlow works on all elements at once. Lists of data need to be kept in special Tensor objects (which accept numpy arrays as inputs). Operations like add, subtract, and multiply are overloaded on Tensors. Behind the scenes when you add/subtract/multiply Tensors it breaks up the data into smaller chunks and the work is farmed out to the GPUs in parallel. There is overhead to do this though, and the CPU bears the brunt of that. If your data set is small, the GPU approach will actually run slower. As the data set grows the GPU will eventually prove to be much more efficient and make tasks possible that were previously unfeasible with CPU only.

def tensor_create(a,b,device="mps") -> (float):
    """Create a tensor matrix of size 2x3 filled with a specific value, e.g., 7."""
    func_time_strt = func_timer_strt()

    tensor_x = torch.full((int(a),int(b)),7)
    tensor_y = torch.full((int(a),int(b)),7)
    tensor_z = tensor_x + tensor_y

    # print(f"x={tensor_x} + y={tensor_y} = z={tensor_z}")

    elapsed_secs = func_timer_stop(func_time_strt)
    return tensor_z, elapsed_secs

def tensor_multiply(device="mps"):
    """Sample tensor multiplication."""
    # Any model.to(device) and tensor to(device) calls work exactly the same with "mps" as with "cuda".
    print(f"\nTASK 1: x+y=z tensor operation on GPU device: \"{device}\" ")
    x = torch.tensor([1.0, 2.0, 3.0], device=device)
    y = torch.tensor([4.0, 5.0, 6.0], device=device)
    z = x + y
    print(f"x={x}")
    print(f"y={y}")
    print(f"z={z}")


# Example: allocate:
    # x = torch.ones(5, device=device)
    # Model example
    #model = YourModelClass().to(device)
    #y = model(x)

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


if __name__ == '__main__':

    SHOW_VERBOSE = True
    SHOW_DEBUG = True
    SHOW_SUMMARY = True
    print("\n# Program command variables: ")
    print(f"    -v  SHOW_VERBOSE={SHOW_VERBOSE}")
    print(f"    -vv SHOW_DEBUG={SHOW_DEBUG}")
    print(f"    -s  SHOW_SUMMARY={SHOW_SUMMARY}")


    local_timestamp = gen_local_timestamp()
    if SHOW_DEBUG:
        pgm_strt_mem_used, pgm_process = pgm_memory_used()
        print(f"DEBUG: {pgm_process}")
        print("DEBUG: pgm_memory used()="+str(pgm_strt_mem_used)+" MiB being used.")
        user_gb_mem_avail = user_gb_mem_avail()
        print(f"DEBUG: user_gb_mem_avail()={user_gb_mem_avail:.2f} GB")
        pgm_strt_disk_free = pgm_diskspace_free()
        print(f"DEBUG: pgm_diskspace_free()={pgm_strt_disk_free:.2f} GB")
        # list_disk_space_by_device()

    # FIXME: my_waveform, rate = wav_shape_rate_torchaudio()
    # FIXME: my_label = sound_from_torchaudio()

    device = chip_device_to_use()

    # See https://www.geeksforgeeks.org/deep-learning/how-to-use-gpu-acceleration-in-pytorch/
    # Move models/tensors to a target device:
    #target_device = torch.device("cuda:1")
    #model = model.to(target_device)
    #tensor = tensor.to(target_device)

    # TODO: Do different runs of this program using different devices:
    device_to_use = "cpu"   # "mps" or "cpu" or "cpu"
    a = 3000
    b = 5000
    processing = "multiply"

    if processing == "multiply":
        data_points = a * b
    func_strt_mem_used, pgm_process = pgm_memory_used()
    if SHOW_DEBUG:
        print(f"DEBUG: {pgm_process}")
        print("DEBUG: pgm_memory used()="+str(func_strt_mem_used)+" MiB being used.")

    my_tensor, secs = tensor_create(a,b,device_to_use)
        # my_tensor = torch.randn((3, 3))

    if SHOW_DEBUG:
        #print(f"my_tensor.size={my_tensor.size()} ")  # Output: torch.Size([2, 3])
        print(f"INFO: tensor_create({a},{b},\"{device_to_use}\") => {secs:.9f} seconds")
    # results(platform, device, data_points, secs )

    func_stop_mem_used, process_data = pgm_memory_used()
    func_stop_mem_diff = func_stop_mem_used - func_strt_mem_used
    if SHOW_DEBUG:
        print(f"{func_stop_mem_diff:.6f} MB memory consumed during run in {process_data}.")

    print("\n# assemble results:")
    print("utc_stamp,data_points,secs,mem_used")
    print(gen_utc_timestamp()+","+str(data_points)+","+device_to_use+\
          ","+processing+","+str(secs)+","+str(func_stop_mem_diff))
    # plot results:


    func_time_strt = func_timer_strt()
    device_to_use = "cpu"   # "mps" or "cpu" or "cpu"
    tensor_multiply(device_to_use)  # 3D math
    elapsed_secs = func_timer_stop(func_time_strt)
    print(f"INFO: tensor_multiply(\"{device_to_use}\") => {elapsed_secs:.9f} seconds")

    # summarizing values in an array (map / reduce)
    # RAG vectors
    # image processing (images are arrays of pixels)
    # machine learning which uses a combination of the above.

    # TODO: Additional sample code from:
    # https://github.com/pytorch/examples
    # https://learning.oreilly.com/library/view/hands-on-machine-learning/9798341607972/
    # https://github.com/ageron/handson-mlp = Hugging Face libraries to download datasets and pretrained models, including transformer models. Transformers are incredibly powerful and versatile, and they are the main building block of virtually all AI assistants today. 

    # Using with BERT
        # https://www.youtube.com/watch?v=uYas6ysyjgY GPU-Acceleration for PyTorch on M1 Macs!
        # https://www.youtube.com/watch?v=-TOdEjcFldI

    #if SHOW_SUMMARY:
    print("TODO: Summary line graph of response times as run n increase.")
    loops_count = 0   # TODO: update
    pgm_summary(pgm_strt_datetimestamp, loops_count)

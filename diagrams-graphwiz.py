#!/usr/bin/env python3

"""diagrams-graphwiz.py here.

https://github.com/wilsonmar/python-samples/blob/main/diagrams-graphwiz.py

Generate diagrams from text after brew install Graphviz.

Based on https://diagrams.mingrammer.com/docs/getting-started/installation

# Usage in CLI to get program source on your laptop:
    brew install graphviz or choco install graphviz # on Windows
    git clone https://github.com/wilsonmar/python-samples --depth 1
    cd python-samples

# Cleanup:
    rm -rf .venv venv
    rm pyproject.toml vu.lock

# Initialize for this program:
    uv init --no-readme.  # create pyproject.toml
    uv venv .venv    # --python python3.12   # for Tensorflow
    source .venv/bin/activate

    chmod +x diagrams-graphwiz.py
    ruff check diagrams-graphwiz.py  # contains Flake8, Pylint, Xenon, Radon, Black, isort, pyupgrade.
    pip install -r requirements.txt

    uv add diagrams, requests

    uv run diagrams-graphwiz.py
    deactivate
"""

__last_change__ = "25-09-16 v001 + create from blog :diagrams-graphwiz.py"
__status__ = "working. Not referencing myutils.py"

import os
import time
from datetime import datetime, timezone
from pathlib import Path

# import requests
# import urllib.request

try:  # external libraries from pypi.com:
    # from _typeshed import FileDescriptorOrPath
    # from typing import Union
    # FileDescriptorOrPath = Union[int, os.PathLike]

    # clusters:
    from diagrams import Cluster, Diagram  # , Edge

    # alibaba cloud resources: https://diagrams.mingrammer.com/docs/nodes/alibabacloud
    # from diagrams.alibabacloud.compute import ECS
    # from diagrams.alibabacloud.storage import ObjectTableStore
    # from diagrams.aws.compute import EC2, ECS, EKS, Lambda
    # from diagrams.aws.database import RDS, ElastiCache, Redshift
    # from diagrams.aws.integration import SQS
    # from diagrams.aws.network import ELB, VPC, Route53
    # https://diagrams.mingrammer.com/docs/nodes/digitalocean
    # aws resources: https://diagrams.mingrammer.com/docs/nodes/aws
    # from diagrams.aws.storage import S3
    # azure resources: https://diagrams.mingrammer.com/docs/nodes/azure
    # from diagrams.azure.compute import FunctionApps
    # from diagrams.azure.storage import BlobStorage
    # Custom: https://diagrams.mingrammer.com/docs/nodes/custom
    from diagrams.custom import Custom

    # Firebase: https://diagrams.mingrammer.com/docs/nodes/firebase
    # Generic: https://diagrams.mingrammer.com/docs/nodes/generic
    # gcp resources: https://diagrams.mingrammer.com/docs/nodes/gcp
    # from diagrams.gcp.compute import GKE, AppEngine
    # from diagrams.gcp.ml import AutoML
    # from diagrams.k8s.chaos import ChaosMesh, LitmusChaos

    # k8s resources:
    # from diagrams.k8s.compute import Pod, StatefulSet
    # from diagrams.k8s.network import Service
    # rom diagrams.k8s.storage import PV, PVC, StorageClass

    # OCI: https://diagrams.mingrammer.com/docs/nodes/oci

    # oracle resources:
    # from diagrams.oci.compute import Container, VirtualMachine
    # from diagrams.oci.network import Firewall
    # from diagrams.oci.storage import FileStorage, StorageGateway

    # Onprem resources: https://diagrams.mingrammer.com/docs/nodes/onprem
    # https://diagrams.mingrammer.com/docs/guides/edge
    # from diagrams.onprem.aggregator import Fluentd
    # from diagrams.onprem.analytics import Spark
    # from diagrams.onprem.compute import Server
    # from diagrams.onprem.database import PostgreSQL
    # from diagrams.onprem.inmemory import Redis
    # from diagrams.onprem.monitoring import Grafana, Prometheus
    # from diagrams.onprem.network import Nginx
    # from diagrams.onprem.queue import Kafka

    # Programming: https://diagrams.mingrammer.com/docs/nodes/programming

except Exception as e:
    print(f"Python module import failed: {e}")
    # uv run log-time-csv.py
    # print("    sys.prefix      = ", sys.prefix)
    # print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:")
    print("\n  uv venv .venv\n  source .venv/bin/activate\n  uv add ___")
    exit(9)


# TODO: Run-time Parameters:
SHOW_VERBOSE = False
SHOW_DEBUG = True
SHOW_SECRETS = False
SECS_BETWEEN_TRIES = 5


def day_of_week(local_time_obj) -> str:
    """Return day of week name from number."""
    # str(days[local_time_obj.weekday()])  # Monday=0 ... Sunday=6
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return str(days[local_time_obj.weekday()])


def timestamp_local() -> str:
    """Generate a timestamp straing containing the local time with AM/PM & Time zone code."""
    # import pytz
    # now = datetime.now(tz)  # adds time zone.

    # from datetime import datetime
    local_time_obj = datetime.now().astimezone()
    local_timestamp = local_time_obj.strftime(
        "%Y-%m-%d_%I:%M:%S %p %Z%z"
    )  # local timestamp with AM/PM & Time zone codes
    enhanced = str(local_timestamp) + " " + day_of_week(local_time_obj)
    return enhanced


def timestamp_utc() -> str:
    """Generate a timestamp straing containing the UTC "Z" time with no AM/PM & Time zone code."""
    # import time
    timestamp = time.time()  # UTC epoch time.
    # from datetime import datetime, timezone
    # Get the current UTC time as a timezone-aware datetime object
    now_utc = datetime.now(timezone.utc)
    # Format the UTC timestamp as a string, e.g., ISO 8601 format
    timestamp = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ") + " " + day_of_week(now_utc)
    return timestamp


def filepath_audit(filepath) -> str:
    """Convert tilde in first character of path."""
    if filepath.startswith("~/"):
        adjusted_filepath = os.path.expanduser("~") + filepath.replace(filepath[0], "", 2)
    elif filepath.startswith("$HOME/"):
        adjusted_filepath = os.path.expanduser("~") + filepath.removeprefix("$HOME/")  # Python 3.9+
    else:
        adjusted_filepath = filepath

    if SHOW_DEBUG:
        print(f"filepath_audit({filepath}) = {adjusted_filepath} ")
    return adjusted_filepath


def load_env_variable(variable_name, env_file="~/python-samples.env") -> str:
    """Retrieve a variable from a .env file in Python without the external dotenv package.

    USAGE: my_variable = load_env_variable('MY_VARIABLE')
    Instead of like: api_key = os.getenv("API_KEY")
    """
    home_path_env = filepath_audit(env_file)
    env_path = Path(home_path_env)
    if SHOW_VERBOSE:
        print(f"VERBOSE: env_path={env_path}")
    if env_path.is_file() and env_path.exists():
        if SHOW_DEBUG:
            print(f"DEBUG: file {env_path} found.")
    else:
        print(f"ERROR: .env file {env_path} is not accessible")
        return None

    with open(env_path) as file:
        # FIXME: FileNotFoundError: [Errno 2] No such file or directory: 'Users/johndoe/python-samples.env'
        for line in file:
            # Strip whitespace and ignore comments or empty lines:
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            # Split the line into key and value:
            key_value = line.split("=", 1)
            if len(key_value) != 2:
                continue

            key, value = key_value
            if key.strip() == variable_name:
                return value.strip().strip('"').strip("'")
    return None


def dir_tree_list(start_path):
    """List directory tree."""
    # USAGE: dir_tree_list('.')
    # import os
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")


def disk_bytes_in_filepath(filepath: str) -> int:
    """Return integer bytes from the OS for a file path."""
    try:
        # import os
        file_bytes = os.path.getsize(filepath)
        return file_bytes
        # Alternately:
        # stat_result = os.stat(filepath)
        # return stat_result.st_blocks * 512  # st_blocks is in 512-byte units
    except FileNotFoundError:
        print(f"ERROR: File path {filepath} not found!")
        return 0
    except Exception as e:
        print(f"FAIL: disk_bytes_in_filepath(): {e}")
        return 0


def file_raw_size(filepath) -> int:
    """Return the size of a file, in bytes.

    If it's a symlink, return 0.
    Called by format_bytes() to format number output.
    """
    # import os
    if os.path.islink(filepath):
        return 0
    return os.path.getsize(filepath)


def bytes_text(num_bytes, show_mib=True, show_mb=True) -> str:
    """Format raw bytes to MiB, MB or GiB, GB."""
    if SHOW_DEBUG:
        gib = 1024**3  # 2^30
        gb = 1000**3  # 10^9
        print(f"bytes_text(): GiB={gib:,d}, GB={gb:,d}")  # decimals

    if show_mib:
        if num_bytes > gib:
            size_gib = num_bytes / gib
            bytes_txt = f"{size_gib:.2f}GiB"
            bytes_txt += "="
        else:
            size_mib = num_bytes / (1024**2)
            bytes_txt = f"{size_mib:.2f}MiB"
            bytes_txt += "="
    if show_mb:
        if num_bytes > gb:
            size_gb = num_bytes / gb
            bytes_txt += f"{size_gb:.2f}GB"
        else:
            size_mb = num_bytes / (1000**2)
            bytes_txt += f"{size_mb:.2f}MB"
    # 9.86MiB=10.34MB
    return bytes_txt


def project_folderpath():
    """Get project folder path from .env or pgm parm.

    Usage: proj_folderpath = project_folderpath()
    """
    # Example in .env file: DIAGRAMS_PATH="./diagrams"
    folderpath_var = "DIAGRAMS_PATH"
    folderpath_in = load_env_variable(folderpath_var)
    folderpath = filepath_audit(folderpath_in)
    if not folderpath:
        print(f"FATAL: {folderpath_var} environment variable not set!")
        return None
    if SHOW_VERBOSE:
        print(f"VERBOSE: .env {folderpath_var}={folderpath}")

    # Create folderpath if it doesn't exist:
    # See https://www.geeksforgeeks.org/python/how-to-create-directory-if-it-does-not-exist-using-python/
    # import os
    if not os.path.exists(folderpath):
        # Also create missing parent folders automatically:
        os.makedirs(folderpath)

    return folderpath


if __name__ == "__main__":
    # if SHOW_VERBOSE:
    #    print(f"diagrams __version__ = {diagrams.__version__}")

    proj_folderpath = project_folderpath()
    if not proj_folderpath:
        print("No proj_folderpath")
        exit()
    else:
        print(f"proj_folderpath={proj_folderpath}")

    my_diagram_name = "AWS-diagram1"
    my_fileroot = my_diagram_name  # no file type ext
    outformats = ["png"]  # ["png", "jpg", "svg", "pdf", "dot"]
    show_diagram = False

    # See https://www.graphviz.org/doc/info/attrs.html
    graph_attr = {  # graph attributes:
        "fontsize": "15",
        "bgcolor": "transparent",
    }
    # node_attr = {}
    # edge_attr = {}

    # Draw diagram:
    # https://diagrams.mingrammer.com/docs/guides/diagram
    # from diagrams.aws.compute import EC2
    for my_outformat in outformats:
        my_diagram_output_basename = proj_folderpath + "/" + my_fileroot
        with Diagram(
            my_diagram_name,
            graph_attr=graph_attr,
            filename=my_diagram_output_basename,
            outformat=my_outformat,
            show=show_diagram,
            direction="LR",
        ):
            # https://creativecommons.org/about/downloads/
            ### Indent:
            cc_heart = Custom("Creative Commons", "./my_resources/cc_heart.black.png")
            cc_attribution = Custom("Credit must be given to the creator", "./my_resources/cc_attribution.png")

            cc_sa = Custom("Adaptations must be shared\n under the same terms", "./my_resources/cc_sa.png")
            cc_nd = Custom("No derivatives or adaptations\n of the work are permitted", "./my_resources/cc_nd.png")
            cc_zero = Custom("Public Domain Dedication", "./my_resources/cc_zero.png")

            with Cluster("Non Commercial"):  # under with Diagram
                non_commercial = [
                    Custom("Y", "./my_resources/cc_nc-jp.png")
                    - Custom("E", "./my_resources/cc_nc-eu.png")
                    - Custom("S", "./my_resources/cc_nc.png")
                ]

            cc_heart >> cc_attribution
            cc_heart >> non_commercial
            cc_heart >> cc_sa
            cc_heart >> cc_nd
            cc_heart >> cc_zero
            # Source indented above this line.
        my_filepath = my_diagram_output_basename + "." + my_outformat
        filesize = file_raw_size(my_filepath)
        print(f"{my_filepath} created: {bytes_text(filesize)}")

    # diag  # draw diagram!

    # List tree and files:
    if proj_folderpath:
        dir_tree_list(proj_folderpath)
    # find . -iname "*FirstDiagram*" -type f 2>/dev/null
    # Files containing: grep -r "FirstDiagram" . 2>/dev/null

# https://diagrams.mingrammer.com/docs/getting-started/examples

#!/usr/bin/env python3
"""local-git.py.

Initializes a bare git repo server and provides utilities to:
- Get the SHA of any file before editing
- Commit files with SHA tracking


BEFORE RUNNING, on internet browser:
   At https://platform.claude.com/settings/organization click "Set up organization".
   Answer questions about country, usage, etc. Submit to "Allow creating new API keys in default workspace".
   At https://platform.claude.com/settings/admin-keys click "Create admin key". Name such as "admin261231"
   Click "Copy key" and paste in your secrets manager or file ~/.secrets.env specified in .gitignore.
   The value is retrieved by code as api03="supersecret"
   ANTHROPIC_ADMIN_KEY="sk-ant-admin01-..." from console by org admins
   ANTHROPIC_API_KEY="sk-ant-api03-..."
   # POLICY: On the CLI Terminal, do not export system variables containing sensitive values, so they are not stored in CLI logs.

BEFORE RUNNING, on Terminal:
   # POLICY: Create a folder for git clone repositories to be created.
   git clone https://github.com/wilsonmar/python-samples.git --depth 1
   cd python-samples
   # uv init was run to set pyproject.toml & .python-version
   python3 -m pip install uv
   python -m venv .venv   # creates bin, include, lib, pyvenv.cfg
   uv venv .venv
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   # POLICY: Add vulnerability scanning utilities. Fail if pyproject.toml and uv.lock are out of sync.
   uv add bandit safety semgrep dynaconf --frozen  # instead of pip install of utilities
   # POLICY: In production, uv sync --frozen --no-build installs project dependencies exactly as specified in the lockfile, without allowing any changes, with --no-build from source, only from pre-built .whl (wheel) executable binaries.

   ruff check local-git.py
   bandit -r ./my_project          # Security linter
   safety scan local-git.py   # Check dependencies in pyproject.toml for bad CVEs
   semgrep --config=auto .         # Pattern-based analysis

   chmod +x local-git.py

BEFORE RUNNING, on Terminal EVERY TIME:
   uv run local-git.py -v -vv 
      # -v for verbose, -b for bill (stats), -sl --sizelimit of code in bytes "1gb"
      # OPTIONAL: -pt for --prompt, -i --iterative, -r --recursive,
      # -f for file to --target for scanning (at end of CWD: /Users/johndoe/github-wilsonmar/python-samples/)
           # Not specifying -f would result in this program processing all .py files in the current folder
      # -m for --model ID recognized by Claude ("claude-opus-4-7" or "claude-sonnet-4-20250514")
      # --nometric to not write csv file of results for each call.
      # Avg run time: Terminal should not freeze.
   # Press control+C to cancel/interrupt run.

AFTER RUN:
    deactivate  # uv
    rm -rf .venv .pytest_cache __pycache__

"""
#### SECTION 02: Dundar variables for git command gxp to git add, commit, push

# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-04-24"
__commit_msg__ = "26-04-24 v001 new @local-git.py"
#__repository__ = "https://github.com/bomonike/google/blob/main/local-git.py"
__repository__ = "https://github.com/wilsonmar/python-samples/blob/main/local-git.py"
__status__ = "WORKING: ruff check local-git.py => All checks passed!"
# STATUS: Python 3.13.3 working on macOS Sequoia 15.3.1

# based on https://github.com/trkonduri/vulscan/blob/master/local-git.py

import subprocess
#import os
import hashlib
from pathlib import Path


# ── Configuration ────────────────────────────────────────────────────────────

REPO_SERVER_DIR = Path.home() / "local-git" / "myproject.git"
WORKING_DIR     = Path.home() / "projects" / "myproject"


# ── Server Setup ─────────────────────────────────────────────────────────────

def init_git_server(server_path: Path = REPO_SERVER_DIR) -> None:
    """Create a bare git repository (the 'server')."""
    server_path.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "init", "--bare", str(server_path)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"[OK] Bare repo initialized at: {server_path}")
    else:
        print(f"[ERROR] {result.stderr}")


def clone_from_server(
    server_path: Path = REPO_SERVER_DIR,
    working_path: Path = WORKING_DIR
) -> None:
    """Clone the bare repo into a working directory."""
    working_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "clone", str(server_path), str(working_path)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"[OK] Cloned to working dir: {working_path}")
    else:
        print(f"[ERROR] {result.stderr}")


# ── SHA Utilities ─────────────────────────────────────────────────────────────

def get_git_sha(file_path: str, working_path: Path = WORKING_DIR) -> str | None:
    """Get the git blob SHA of a tracked file (as stored in git's object DB).

    This is the SHA git uses internally — matches `git hash-object <file>`.
    Returns None if the file is untracked or the path is invalid.
    """
    result = subprocess.run(
        ["git", "ls-files", "-s", file_path],
        capture_output=True, text=True, cwd=working_path
    )
    if result.stdout.strip():
        # Format: <mode> <sha> <stage>\t<file>
        sha = result.stdout.split()[1]
        return sha
    return None


def get_blob_sha(file_path: str, working_path: Path = WORKING_DIR) -> str:
    """
    Compute the git blob SHA of a file (even if untracked).

    Equivalent to: git hash-object <file>
    """
    result = subprocess.run(
        ["git", "hash-object", file_path],
        capture_output=True, text=True, cwd=working_path
    )
    return result.stdout.strip()


def get_raw_sha256(file_path: str) -> str:
    """SHA-256 of the raw file bytes (not git's blob SHA — useful as a bonus check)."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_before_edit(file_path: str, working_path: Path = WORKING_DIR) -> dict:
    """
    Call this BEFORE editing a file.

    Returns a dict with both the git blob SHA and raw SHA-256.
    """
    abs_path = working_path / file_path

    git_sha   = get_git_sha(file_path, working_path)
    blob_sha  = get_blob_sha(str(abs_path), working_path)
    raw_sha   = get_raw_sha256(str(abs_path)) if abs_path.exists() else None

    info = {
        "file":         file_path,
        "git_tree_sha": git_sha,   # SHA from git index (None if untracked)
        "git_blob_sha": blob_sha,  # git hash-object result
        "sha256":       raw_sha,   # raw file SHA-256
    }

    print(f"\n📄 File       : {file_path}")
    print(f"   git SHA    : {git_sha  or '(untracked)'}")
    print(f"   blob SHA   : {blob_sha or '(not found)'}")
    print(f"   SHA-256    : {raw_sha  or '(not found)'}")
    return info


# ── Workflow Helpers ──────────────────────────────────────────────────────────

def stage_and_commit(
    file_path: str,
    message: str,
    working_path: Path = WORKING_DIR
) -> str:
    """Stage a file, commit it, and return the commit SHA."""
    subprocess.run(["git", "add", file_path], cwd=working_path, check=True)

    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True, cwd=working_path
    )
    print(result.stdout.strip())

    # Return the new commit SHA
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=working_path
    ).stdout.strip()
    print(f"[OK] Commit SHA: {sha}")
    return sha


def push_to_server(working_path: Path = WORKING_DIR) -> None:
    """Push local commits back to the bare server repo."""
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True, text=True, cwd=working_path
    )
    print(result.stdout.strip() or result.stderr.strip())


# ── Demo ──────────────────────────────────────────────────────────────────────

def demo():
    """Demo run."""
    print("=== Setting up local git server ===\n")

    # 1. Init bare server repo
    init_git_server()

    # 2. Clone to working directory
    clone_from_server()

    # 3. Create a sample file
    sample = WORKING_DIR / "hello.py"
    sample.write_text('print("hello world")\n')

    # 4. Initial commit so git tracks the file
    subprocess.run(
        ["git", "add", "hello.py"],
        cwd=WORKING_DIR, check=True
    )
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "init: add hello.py"],
        cwd=WORKING_DIR, check=True
    )

    # 5. Get SHA before editing — your workflow entry point
    info = sha_before_edit("hello.py")

    # 6. Simulate editing the file
    sample.write_text('print("hello world — edited")\n')

    # 7. Commit the edit and push
    stage_and_commit("hello.py", "feat: update greeting")
    push_to_server()

    print("\n=== Done. SHAs recorded before and after edit. ===")
    return info


if __name__ == "__main__":
    demo()

"""
./local-git.py -v -vv 
=== Setting up local git server ===

[OK] Bare repo initialized at: /Users/johndoe/local-git/myproject.git
[OK] Cloned to working dir: /Users/johndoe/projects/myproject
[master (root-commit) ca99f5e] init: add hello.py
 1 file changed, 1 insertion(+)
 create mode 100644 hello.py

📄 File       : hello.py
   git SHA    : 8cde7829c178ede96040e03f17c416d15bdacd01
   blob SHA   : 8cde7829c178ede96040e03f17c416d15bdacd01
   SHA-256    : 4660ab1ff310887b8f4727933f68eeb74012a5fbc7107d500b146796f0d95b6b
[master a4cc407] feat: update greeting
 1 file changed, 1 insertion(+), 1 deletion(-)
[OK] Commit SHA: a4cc407552060c76e7503aadffe0a5cf39d2a716
error: src refspec main does not match any
error: failed to push some refs to '/Users/johndoe/local-git/myproject.git'

=== Done. SHAs recorded before and after edit. ===
"""

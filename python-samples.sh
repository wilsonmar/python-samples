#!/usr/bin/env bash
# This is python-samples.sh within https://github.com/wilsonmar/python-samples
# run to install and update external Python packages (dependencies) needed by "import" statements in the code.
# (to avoid ModuleNotFoundError: No module named ... )

THIS_PROGRAM="$0"
SCRIPT_VERSION="v0.0.12"

# After you obtain a Terminal (console) in your enviornment,
# cd to folder, copy this line and paste in the terminal (without the # character):
   # bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/python-samples/master/bash/python-samples.sh)" -v -i

# SECTION 1. Establish shell file run environment
# SECTION 2. Install utilities 
# SECTION 3. Obtain a copy of the repo holding source code and sample files
# SECTION 4. Create a virtual environment to isolate package dependency versions
# SECTION 5. Install pip packages in the enviornment
# SECTION 6. Install and run scans
# SECTION 7. Run Python interpreter on app code (python-samples.py)

# shellcheck disable=SC2001 # See if you can use ${variable//search/replace} instead.
# shellcheck disable=SC1090 # Can't follow non-constant source. Use a directive to specify location.

# ----------------------------------------------------

# SECTION 1. Establish shell file run enviornment

### Set ANSI color variables (based on aws_code_deploy.sh): 
bold="\e[1m"
dim="\e[2m"
# shellcheck disable=SC2034 # ... appears unused. Verify use (or export if used externally).
underline="\e[4m"
# shellcheck disable=SC2034 # ... appears unused. Verify use (or export if used externally).
blink="\e[5m"
reset="\e[0m"
red="\e[31m"
green="\e[32m"
# shellcheck disable=SC2034 # ... appears unused. Verify use (or export if used externally).
blue="\e[34m"
cyan="\e[36m"

h2() { if [ "${RUN_QUIET}" = false ]; then    # heading
   printf "\n${bold}\e[33m\u2665 %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
   fi
}
info() {   # output on every run
   printf "${dim}\n➜ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
note() { if [ "${RUN_VERBOSE}" = true ]; then
   printf "\n${bold}${cyan} ${reset} ${cyan}%s${reset}" "$(echo "$@" | sed '/./,$!d')"
   printf "\n"
   fi
}
success() {
   printf "\n${green}✔ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
error() {    # &#9747;
   printf "\n${red}${bold}✖ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
warning() {  # &#9758; or &#9755;
   printf "\n${cyan}☞ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
fatal() {   # Skull: &#9760;  # Star: &starf; &#9733; U+02606  # Toxic: &#9762;
   printf "\n${red}☢  %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}

RUN_VIRTUALENV=false
RUN_PIPENV=false

run_pytest=false
run_gitleaks=false
run_flake8=false
run_autopep8=false
run_pylint=false
run_bandit=true

# if desired folder is not there, create it:
# cd to desired folder:
# cd project



# SECTION 2. Install utilities  ################################

# see sample.sh
#    1. XCode Command Utilities                   - see https://wilsonmar.github.io/xcode
#    2. Homebrew which installs MacOS utilities:  - see https://wilsonmar.github.io/homebrew
#    3. Homebrew packages: jq, gpg, etc.
#    4. Python IDE (PyCharm or VSCode or Cloud9)  - see https://wilsonmar.github.io/text-editors
#    5. configure IDE plug-ins
#    6. Miniconda virtual environment             - see https://wilsonmar.github.io/python-install
#    7. Python within Miniconda
#    8. The latest git client                     - see https://wilsonmar.github.io/git-install
#    9. AWS CLI                                   - see https://wilsonmar.github.io/aws-cli
#    10. Google Chrome browser and add-ons


# SECTION 3. Obtain a copy of the repo holding source code and sample files

# TODO: Wrap logic around this:
# If repo is there, upgrade it?
    # git clone https://github.com/wilsonmar/python-samples
    # cd python-samples


# SECTION 4. Create a conda environment  ===============================

if [ "${RUN_VIRTUALENV}" = true ]; then  # -V  (not the default pipenv)

   # https://levipy.com/virtualenv-and-virtualenvwrapper-tutorial
   # to create isolated Python environments. https://docs.python.org/3/library/venv.html
   #pipenv install virtualenvwrapper

   my_venv_folder="venv"
   if [ -d ${my_venv_folder} ]; then   # venv folder already in the folder:
      note "Folder {my_venv_folder} being re-used ..."
   else
      # The venv module is included in the Python standard library installed.
      h2 "Make venv ${my_venv_folder} ..."  # venv is for Python3, virtualenv is for Python2
      python3 -m venv "${my_venv_folder}"
      if [ ! -d "${my_venv_folder}" ]; then   # venv folder already in the folder:
         echo "${my_venv_folder} folder not found"
         exit 1
      fi
   fi

   if [ ! -d ${my_venv_folder} ]; then
      h2 "Activate {my_venv_folder}"
      source "${my_venv_folder}/bin/activate"
      # "(venv)" should now appear above the cursor.
   else
      echo "${my_venv_folder} not found. Aborting."
      exit
   fi

   # To check if one a virtual environment is active, check whether the 
   # VIRTUAL_ENV environment variable is set to the path of the virtual environment. 
   echo ${VIRTUAL_ENV}  # /Users/wilson_mar/gmail_acct/python-samples/venv

   # FIXME: -bash: syntax error near unexpected token `('
   # base_prefix=getattr(sys, "base_prefix", None)
      # base_prefix='/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9'
      # sys.prefix='/Users/wilson_mar/gmail_acct/python-samples/venv'
   # echo "${sys.prefix}"
   # if ${my_venv_folder} is found at the end of sys.prefix:


   """
      # TODO: Make sure venv is in .gitignore:
   RESPONSE="$( find "venv" -type d -name *"${GitHub_REPO_NAME}"* )"
   if [ -n "${RESPONSE}" ]; then  # found somethiNg:
      note "${RESPONSE}"
      if [ "${REMOVE_GITHUB_BEFORE}" = true ]; then  # -d 
          ...
      fi
   fi
   """


   

      h2 "source venv/bin/activate"
      # shellcheck disable=SC1091 # Not following: venv/bin/activate was not specified as input (see shellcheck -x).
      source venv/bin/activate

      # RESPONSE=$( python3 -c "import sys; print(sys.version)" )
      RESPONSE=$( python3 -c "import sys, os; is_conda = os.path.exists(os.path.join(sys.prefix, 'conda-meta'))" )
      h2 "Within (venv) Python3: "
      # echo "${RESPONSE}"
     
   if [ -f "requirements.txt" ]; then
      # Created by command pip freeze > requirements.txt previously.
      # see https://medium.com/@boscacci/why-and-how-to-make-a-requirements-txt-f329c685181e
      # Install the latest versions, which may not be backward-compatible:
      pip3 install -r requirements.txt
   fi

fi

if [ "${RUN_PIPENV}" = true ]; then  # -V  (not the default pipenv)

   h2 "Use Pipenv by default (not overrided by -Virtulenv)"
   # https://www.activestate.com/blog/how-to-build-a-ci-cd-pipeline-for-python/

   # pipenv commands: https://pipenv.kennethreitz.org/en/latest/cli/#cmdoption-pipenv-rm
   note "pipenv in $( pipenv --where )"
      # pipenv in /Users/wilson_mar/projects/python-samples
   # pipenv --venv  # no such option¶
   
   note "$( pipenv --venv || true )"

   #h2 "pipenv lock --clear to flush the pipenv cache"
   #pipenv lock --clear

   # If virtualenvs exists for repo, remove it:
   if [ -n "${WORKON_HOME}" ]; then  # found somethiNg:
      # Unless export PIPENV_VENV_IN_PROJECT=1 is defined in your .bashrc/.zshrc,
      # and export WORKON_HOME=~/.venvs overrides location,
      # pipenv stores virtualenvs globally with the name of the project’s root directory plus the hash of the full path to the project’s root,
      # so several can be generated.
      PIPENV_PATH="${WORKON_HOME}"
   else
      PIPENV_PATH="$HOME/.local/share/virtualenvs/"
   fi
   RESPONSE="$( find "${PIPENV_PATH}" -type d -name *"${GitHub_REPO_NAME}"* )"
   if [ -n "${RESPONSE}" ]; then  # found somethiNg:
      note "${RESPONSE}"
      if [ "${REMOVE_GITHUB_BEFORE}" = true ]; then  # -d 
         pipenv --rm
            # Removing virtualenv (/Users/wilson_mar/.local/share/virtualenvs/bash-8hDxYnPf)…
            # or "No virtualenv has been created for this project yet!  Aborted!

         # pipenv clean  # creates a virtualenv
            # uninistall all dev dependencies and their dependencies:

         pipenv_install   # 
      else
         h2 "TODO: pipenv using current virtualenv ..."
      fi
   else  # no env found, so ...
      h2 "Creating pipenv - no previous virtualenv ..."
      PYTHONPATH='.' pipenv run python main.py    
   fi 

fi  # RUN_VIRTUALENV


# SECTION 5. Install pip packages in conda environment  ###################

#    Python packages (dependencies) needed by "import" statements in the code

     # Put these in the requirements.txt file or run the following:

       # https://realpython.com/python-virtual-environments-a-primer/
       # BEWARE https://github.com/Homebrew/homebrew-core/issues/76621
       # -U specifies Update (re-install) when run after initial installation.

       pip install -U python-dotenv  # see https://pypi.org/project/python-dotenv/
       pip install -U argparse  # to parse parameters
       pip install -U textblob  # localizes text using API calls to Google Translate.
       python -m textblob.download_corpora
       pip install -U keyring
       pip install -U azure-identity  # the Azure Active Directory identity library
       pip install -U azure-keyvault-secrets  # the Key Vault secrets library
       pip install -U boto3  # to access AWS (Amazon Web Services)
       pip install -U hvac   # hvac-0.11.2
       pip install google-cloud-secret-manager  # 2.8.0-py2.py3-none-any.whl (94 kB)
       # pip install -U pyjwt   # https://github.com/jpadilla/pyjwt & https://pyjwt.readthedocs.io/en/stable/
       pip install -U redis   # redis-4.0.2-py3-none-any.whl (119 kB)
       sudo pip3 install -U pytz   # installed pytz-2021.3

# SECTION 6. Install and run scans

    # See https://www.securecoding.com/blog/best-python-open-source-security-tools/
    # 1. Unit Testing
   if [ "${run_pytest}" = true ]; then
       pip install -U pytest
       # pytest
   fi
    # 2. GitLeaks
    if [ "${run_gitleaks}" = true ]; then
        pip install -U gitleaks
    fi
    # 3. See https://flake8.pycqa.org/en/4.0.1/user/error-codes.html
    if [ "${run_flake8}" = true ]; then
       pip install -U flake8
       # Run:
       flake8 api-sample.py --ignore E111,E114,E116,E201,E202,E203,E221,E225,E231,E265,E266,E303,E501,W291,W293
    fi
   # 4. Lint program code using https://www.python.org/dev/peps/pep-0008/ and https://github.com/hhatto/autopep8
    if [ "${run_autopep8}" = true ]; then
       pip install -U autopep8
       # Run:
       autopep8 --in-place --aggressive --aggressive api-sample.py
       # Return of nothing means you're good?
    fi
   # 5. pylint which automates https://pylint.org/ = https://google.github.io/styleguide/pyguide.html
    if [ "${run_pylint}" = true ]; then
       pip install -U pylint
       pylint api-sample.py
    fi
   # 6. Pyreverse: UML Diagrams for Python - https://www.logilab.org/blogentry/6883
   # 7. Bandit
    if [ "${run_bandit}" = true ]; then
       pip install -U bandit
    fi

# SECTION 7. Run Python interpreter on app code (api-sample.py)
python api-sample.py

# TODO: Check to see if file already there:
   # If not, copy sample to $HOME and stop


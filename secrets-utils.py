#!/usr/bin/env python3
# https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "argon2-cffi",
#   "cryptography",
#   "fido2",
#   "gnupg",
#   "psutil",
#   "python-dotenv",
#   "pyopenssl",
# ]
# ///

"""secrets-utils.py here.

This program presents a GUI website on a macOS and Linux machine to encrypt text and files, then share them  privately with automatic decryption. 

Why? This does not us 3rd-parties such as Proton Mail, Slack, LinkedIn, Discord, etc.
Because sending anything over the public internet risks interception.
If intercepted, hackers would have unlimited time to brute-force decryption of your secrets.

Gmail does not provide a way for senders to send and recipients to read encrypted messages.

This program provides a convenient and way to generate passwords. Third-party password generators such as
Bitwarden Send or Onetime Secret allow sending encrypted secrets, but any public website has dubious trustability.

Here's how this program works:

1. Start the program by specifying parms to supply the cleartext or the filepath to a file.

2. Alternately, start a GUI web server to present a form to accept the values.

3. Optionally, setup & use 2FA to verify authentication. The Google Titan Key is only for authentication or registration. Secrete data cannot be stored or extracted from it. It's accessed via USB/NFC and communicates using FIDO2/U2F protocols.

4. If available, get a public key published by the recipient, such as at https://keybase.io/santosomar or provide as a filepath (to USB drive)

5. Alternately, generate a static symmetric password (of more than 20 chars) for use by both parties.

6. If a password was generated, share (with no context) a PIN of 6 numbers via phone conversation.

7. Use the Fernet library to encrypt a file using the generated password key.

8. Use the gnupg library to encrypt a file using the PGP public key. GPG (GNU Privacy Guard) is an open-source implementation of the OpenPGP standard RFC 4880.

9. Create the encrypted file in a <strong>removeable USB storage device</strong> for physical transfer of data. The file name can be a GUID such as <tt>9e58528c-ffc3-4bdf-8aa7-973b7dd66420</tt>

10. Optionally, Create a URL on a <strong>web page</strong> for the recipient to retrieve the encrypted file

    This need not be a full-blown FastAPI and NodeJs server because the file made available is proctected by encryption. So the website doesn't have to go throughly authenticate users.

    A colleague within the firewall can use a website created on the sender's machine's IP address such as 
   
    <tt>http://192.168.32.43:8012/9e58528c-ffc3-4bdf-8aa7-973b7dd66420</tt>
   
    on a web server created by: 
   
    <a target="_blank" href="https://medium.com/the-pythonworld/python-has-a-built-in-web-server-heres-how-to-use-it-08c0f17f72f7">python -m http.server 8012</a>  --directory /path/to/folder

    That command references the <tt>http.server</tt> module in Python’s standard library (no import needed):

    <tt>from http.server import SimpleHTTPRequestHandler, HTTPServer</tt>

    This is single-threaded and won’t handle heavy traffic.

11. Generate a <strong>QR code</strong> of the (perhaps <strong>shortened</strong>) URL for recipients to scan for retrieving the secret at the destination.

12. If a key pair is used, Recipient would download this program from github and run this as -recipient to
manually provide the filepath to his/her private key created with the public key used.

13. Optionally, to reduce risk if a channel being compromised, the secret is split so each part is sent via different channels, each with a distinct password key.

14. When recipient accesses the web site, store the IP address of the response associated with the sender along with password in a password manager. Send a reminder if secret was not retrieved within expected time.
15. The URL self-destructs (expires) after being viewed once, to minimize exposure risk.

16. Use two-factor auth, such as setup of Passkey, Yubikey, or One-Time Password (Authy app installed on mobile app).
 
USAGE: To run this program, on a macOS Terminal:
    brew install gnupg   # to /opt/homebrew/bin/gpg
    brew install openssl
    brew install argon2  # for the c_argon2 library needed for Python's argon2-cffi package.

    chmod +x secrets-utils.py
    uv venv .venv
    source .venv/bin/activate
    ruff check secrets-utils.py
    uv run secrets-utils.py -v -vv -ct "My secret"
"""

__last_change__ = "25-10-14 v015 + ARGON2ID hash :secrets-utils.py"
__status__ = "encrypting to .enc not yet tested."

# Built-in libraries:
import argparse
import base64
#import csv
from datetime import datetime, timezone
import hashlib
import math
#import os
from pathlib import Path
# import pytz
import random
import re      # regex
import sys
import time
import uuid

# External libraries:
# fido2-titan.py
import os

try:
    from argon2 import PasswordHasher     # uv pip install argon2-cffi
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    from fido2.hid import CtapHidDevice
    #from fido2.client import Fido2Client
    #from fido2.server import Fido2Server
    # from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity
    #from fido2 import cbor
    #import getpass
    from io import StringIO
    from dotenv import dotenv_values
    import gnupg
    #import inspect
    import psutil
    #import OpenSSL
    import secrets    # uv pip install secrets # for random number (token, key) gen # "secrets-utils",
except Exception as e:
    print(f"Python module import failed: {e}")
    # uv run log-time-csv.py
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print("Please activate your virtual environment:\n  uv venv .venv\n  source .venv/bin/activate")
    exit(9)


# Global static variables:
SHOW_SECRETS = True
SHOW_VERBOSE = True
SHOW_DEBUG = True
SHOW_SUMMARY = True
cleartext = "Hello World!"
enc_file_created = True
create_enc_file = True


# Program Timings:

# For wall time measurements:
pgm_strt_datetimestamp = datetime.now()


def read_cmd_args() -> None:
    """Read command line arguments and set global variables.

    See https://realpython.com/command-line-interfaces-python-argparse/
    """
    #import argparse
    #from argparse import ArgumentParser
    parser = argparse.ArgumentParser(allow_abbrev=True,description="secrets-utils.py")
    parser.add_argument("-q", "--quiet", action="store_true", help="Run without output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show inputs into functions")
    parser.add_argument("-vv", "--debug", action="store_true", help="Debug outputs from functions")
    parser.add_argument("-s", "--summary", action="store_true", help="Show summary stats")

    parser.add_argument("-ct", "--cleartext", action="store_true", help="Cleartext to encrypt/send")
    # Default -h = --help (list arguments)

    args = parser.parse_args()


    #### SECTION 08 - Override defaults and .env file with run-time parms:

    # In sequence of workflow:

    global SHOW_VERBOSE
    global SHOW_DEBUG
    global SHOW_SUMMARY
    global cleartext

    if args.quiet:         # -q --quiet
        SHOW_VERBOSE = False
        SHOW_DEBUG = False
        SHOW_SUMMARY = False

    if args.verbose:       # -v --verbose (flag)
        SHOW_VERBOSE = True
    if args.debug:         # -vv --debug (flag)
        SHOW_DEBUG = True
    if args.summary:       # -s --summary (flag)
        SHOW_SUMMARY = True
    if args.cleartext:      # -ct  --cleartext
        cleartext = args.cleartext

    return None

# USAGE:
# uv run log-time-csv.py -v -vv -ml 0

#### Time Utility Functions:

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

## Memory & Processes Utilities:

def pgm_memory_used() -> (float, str):
    """Return the MiB of RAM for the current process, using the psutil library."""
    #import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    process_info = str(process)
    mem=process.memory_info().rss / (1024 ** 2)  # in z
    return mem, process_info


def pgm_summary(std_strt_datetimestamp, loops_count):
    """Print summary count of files processed and the time to do them."""
    # For wall time of standard imports:
    pgm_stop_datetimestamp = datetime.now()
    pgm_elapsed_wall_time = pgm_stop_datetimestamp - pgm_strt_datetimestamp

    if SHOW_SUMMARY:
        pgm_stop_mem_used, process_data = pgm_memory_used()
        pgm_stop_mem_diff = pgm_stop_mem_used - pgm_strt_mem_used
        print(f"{pgm_stop_mem_diff:.6f} MB memory consumed during run in {process_data}.")

        pgm_stop_disk_diff = pgm_strt_disk_free - pgm_diskspace_free()
        print(f"{pgm_stop_disk_diff:.6f} GB disk space consumed during run.")

        print(f"SUMMARY: Ended while attempting loop {loops_count} in {pgm_elapsed_wall_time} seconds.")
    else:
        print(f"SUMMARY: Ended while attempting loop {loops_count}.")


## URL


def filepath_audit(filepath) -> str:
    """Convert $HOME and tilde in first character of path to user's home folder.
    
    Used by load_env_file() below.
    """
    if filepath.startswith("~/"):
        adjusted_filepath = os.path.expanduser("~") + filepath.replace(filepath[0], "", 2)
    elif filepath.startswith("$HOME/"):
        adjusted_filepath = os.path.expanduser("~") + filepath.removeprefix("$HOME/")  # Python 3.9+
    else:
        adjusted_filepath = filepath

    if SHOW_DEBUG:
        print(f"filepath_audit({filepath}) = {adjusted_filepath} ")
    return adjusted_filepath


## Folders & Files Disk Space Utilities:

def pgm_diskspace_free() -> float:
    """Return the GB of disk space free of the partition in use, using the psutil library."""
    #import os, psutil  #  psutil-5.9.5
    disk = psutil.disk_usage('/')
    free_space_gb = disk.free / (1024 * 1024 * 1024)  # = 1024 * 1024 * 1024
    return free_space_gb

def file_raw_size(filepath) -> int:
    """Return the size of a file, in bytes.

    If it's a symlink, return 0.
    Called by format_bytes() to format number output.
    """
    #import os
    if os.path.islink(filepath):
        return 0
    return os.path.getsize(filepath)

def dir_raw_size(filepath) -> int:
    """Return the size of a directory/folder hierarchy, in bytes.

    Example: filepath="../../github-wilsonmar/python-samples/"
    If it's a symlink, return 0.
    Called by format_bytes() to format number output.
    """
    #import os
    if os.path.islink(filepath):
        return 0

    # If ~ or $HOME is in beginning of filepath, convert it:
    if filepath.startswith("~") or filepath.startswith(filepath.upper("$HOME")):
        filepath = os.path.expanduser(filepath)
        print(f"DEBUG: filepath={filepath}")

    size = 0.0
    for root, _dirs, files in os.walk(filepath):
        for filename in files:
            file_path = os.path.join(root, filename)
            size += file_raw_size(file_path)
    return size

def file_divide(filepath_in, outfile_a, outfile_b):
    """Split a file into two files."""   
    # Open the large file in read mode:
    with open(filepath_in, 'r') as file:
        lines = file.readlines()  # Read all lines into a list

    # Write the first half of lines to a new file:
    with open(outfile_a, 'w') as file1:
        for line in lines[:len(lines)//2]:
            file1.write(line)

    # Write the second half of lines to another new file:
    with open(outfile_b, 'w') as file2:
        for line in lines[len(lines)//2:]:
            file2.write(line)


def format_bytes(bytes_value, show_mib=True, show_mb=True) -> str:
    """Format bytes in MiB and MB.
    
    TODO: GiB & GB for larger numbers.
    """
    if show_mib:
        size_mib = bytes_value / (1024 ** 2)
        bytes_txt = f"{size_mib:.2f}MiB"
        bytes_txt += "="
    if show_mb:
        size_mb = bytes_value / (1000 ** 2)
        bytes_txt += f"{size_mb:.2f}MB"
    # 9.86MiB=10.34MB
    return bytes_txt

# TODO: zip
# TODO: unzip

def pgm_fda_test() -> bool:
    """Return True if this program has FDA (Full Disk Access) on macOS.
    
    Although there is no official macOS API or direct Python method to programmatically detect if an app has Full Disk Access (FDA), Apple recommends a trial approach: read a known protected file that requires FDA, such as /Library/Preferences/com.apple.TimeMachine.plist. If access to this file fails, it indicates the app does not have Full Disk Access.
    """
    try:
        # macOS only:
        with open("/Library/Preferences/com.apple.TimeMachine.plist", "rb") as f:
            f.read(1)  # Try reading some bytes
        print("VERBOSE: pgm_fda_test() can!")
        return True
    except PermissionError:
        print("VERBOSE: pgm_fda_test() does NOT have macOS Full Disk Access!")
        return False


### Random Numbers:

def random_num(byte_size, algorithm="random") -> int:
    """Generate a cryptographically strong random number of a size requested.

    secrets library utilizes the operating system's source of randomness, more secure than random module.
    If you aren't using libsodium:
    If you need random bytes, use os.urandom().
    If you need other forms of randomness, you want an instance of 
    See https://github.com/sobolevn/awesome-cryptography
    Based on https://paragonie.com/blog/2016/05/how-generate-secure-random-numbers-in-various-programming-languages#python-csprng
    # Does not use Deterministic Random Bit Generators (DRBGs) - NIST SP 800-90A Rev. 2 https://csrc.nist.gov/pubs/sp/800/90/a/r2/final
    """        
    #algorithm = "random"
    #algorithm = "urandom"
    # algorithm = "randbelow"
    #algorithm = "randbits"
    # print(f"VERBOSE: {algorithm} random_num({byte_size},max_val= {sys.maxsize}")
    if algorithm == "random":   # not cryptographically secure.
        # import sys
        # import random
        csprng = random.SystemRandom()   # instead of just random.
        random_int = csprng.randint(0, sys.maxsize)

    elif algorithm == "urandom":
        # import os   # cryptographically secure pseudo-random number generator (CSPRNG)
        # from unpredictable hardware events like mouse movements, network traffic, and interrupt timings. 
        # WARNING: os.urandom() on Linux uses the getrandom() syscall without the GRND_NONBLOCK flag.
        # So it can block if the system's entropy pool has not yet accumulated enough randomness to ensure the quality of the generated data.
        bits = byte_size // 2   # round down to divisors of 8.
        raw_bytes = os.urandom(int(bits))

        # PROTIP: Convert raw bytes to hex:
        # import binascii
        # hex_key = binascii.hexlify(raw_bytes) 

        # PROTIP: Convert raw bytes to integer:
        random_int = int.from_bytes(raw_bytes, byteorder='big')

    elif algorithm == "randbits":
        # Generate a secure random integer with k random bits (of random size):
        bits = byte_size // 2 * 8    # // to round down to divisors of 8.
        print(f"VERBOSE: randbits({byte_size} digits={bits} bits for {algorithm})")
        # import secrets
        random_int = secrets.randbits(int(bits))

    elif algorithm == "randbelow":
        # secrets.randbelow(100) Generates a random integer between 0 and 99 (inclusive):
        all9s = '9' * byte_size
        # import secrets
        random_int = secrets.randbelow(int(all9s))

    else:
        print(f"FATAL: random_num() algorithm {algorithm} unrecognized!")

    random_digits = len(str(random_int))
    print(f"INFO: random_num({byte_size} digits, \"{algorithm}\"): {random_int} ")
    return random_digits


def gen_uuid_rand() -> str:
    """Generate random UUID (Universally Unique Identifier) version 4."""
    # uuid4() are completely random and does not expose MAC addresses.
    # See https://blog.stephencleary.com/2010/11/few-words-on-guids.html
    #import uuid  #built-in
    return str(uuid.uuid4())

def gen_uuid_seq() -> str:
    """Generate sequential UUID (Universally Unique Identifier) version 1."""
    # uuid1() RFC 4122 are 128-bit (16-byte) 92eb03f5-3ba0-4d95-960f-c6c084c93374 
    # UUID1 includes a 60-bit UTC timestamp, 14-bit clock sequence, and 48-bit node identifier, 
    # uuid1 are time-ordered and unique across machines and exposes MAC addresses.
    # See https://blog.stephencleary.com/2010/11/few-words-on-guids.html
    #import uuid  #built-in
    return str(uuid.uuid1())


def shannon_entropy(data):
    """Count frequency of each byte value (0-255) for entropy of 0 to 8."""
    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1
    data_len = len(data)
    
    entropy = 0.0
    for count in byte_counts:
        if count == 0:
            continue
        p = count / data_len
        entropy -= p * math.log(p, 2)  # log base 2 for entropy in bits
    return entropy
    # How about dividing 4.782 / 8 for like 59.1%?


### Hashing

def hash_txt(cleartext, hash_type):
    """Hashes the cleartext using the specified hash_type."""
    # These automatically use a random salt.
    if hash_type.upper() == "ARGON2ID":   # 97 char.
        # Hash algorithms that resist brute-force attacks:
        # "Argon2" uses argon2-cffi - the top choice, winner of the Password Hashing Competition.
        #from argon2 import PasswordHasher.   # pip install argon2-cffi
        # Defaults to Argon2id which combines Argon2d and Argon2i
        # Many options. See https://cryptobook.nakov.com/mac-and-key-derivation/argon2
        # v=, m=memory, t=iterations,p=parallelism threads

        # from argon2 import PasswordHasher
        # Create a password hasher instance: 
        ph = PasswordHasher()
        hashed = ph.hash(cleartext)
        # TODO: "script" when Argon2 is not available.
        return hashed
    elif hash_type == "SHA256":
        return hashlib.sha256(cleartext.encode()).hexdigest()
    elif hash_type == "SHA512":
        return hashlib.sha512(cleartext.encode()).hexdigest()
    elif hash_type == "MD5":
        return hashlib.md5(cleartext.encode()).hexdigest()
    else:
        print(f"FATAL: Unsupported hash_type: {hash_type}")
        return None


### Encryption/Decryption

# https://www.howtogeek.com/734838/how-to-use-encrypted-passwords-in-bash-scripts/


def passkey(platform_id) -> str:
    """Enable Flask app to use Passkeys by known platforms to manage registration and login.

    Leverage FIDO2-certifiedWebAuthn API library or a Passkeys service API:
       * Hanko Cloud Passkey https://www.hanko.io/blog/passkeys-python-flask & https://github.com/teamhanko/passkeys-python See https://docs.hanko.io/passkey-api/introduction
       * Corbado
    See https://www.wired.com/story/what-is-a-passkey-and-how-to-use-them/
    known platforms list at https://passkeys.2fa.directory/us/ from Sweden
    Open-source examples: GitHub repos for Autsec-Passkey or Hanko Passkeys Python Flask integration)
    1. Create URL to a (Flask or Django) website where passkeys will be bound to.
    2. On website, user clicks "Sign up" to create account after verifying email address with a OTP.
    3. On vendor website, user creates a passkey for the platform being used (Apple, Android, Windows, etc.)
    4. On platform: Apple, "Use Touch ID to sign in" and create Organization, Hanko project etc.
    5. On Hanko cloud, create project with URL.
    6. Copy PASSKEY_TENANT_ID from website to .env file (in user $HOME).
    7. Create PASSKEY_API_KEY and past into .env file.

    8. On GUI, user clicks "Sign in with a passkey" to show QR code.
    9. User uses smartphone to scan QR to "Sign in with a passkey" URL to backend endpoint.
    10. Complete registration: Backend verifies client response and stores key.

    11. Start login: User begins login call to backend.
    12. Complete login: Backend verifies authentication response.
    """
    platform_id = platform_id.upper()
    # Google Password Manager, Microsoft Windows Hello, Apple, etc.
    # with biometric face, fingerprint, or PIN.
    # Android 9 or newer
    # iOS 16 or newer 
    # macOS 13 (Ventura) or newer on Apple iCloud Keychain using the Passwords app
    # Windows 10/11 23H2 or newer prompts you to use a passkey whenever you attempt to sign in

    passkey = ""
    # The best implementations of passkeys don’t even need a username.
    return passkey


def fido2_secret(use_salt=False) -> str:
    """Read and return FIDO2 key ID number for use as a key for symmetric encryption."""
    try: 
        # TECHNIQUE: List all CTAP HID devices
        # print("VERBOSE: fido2_secret(): list FIDO2 devices:")
        devices = list(CtapHidDevice.list_devices())
        if not devices:
            # print(f"DOTHIS: Please insert a FIDO Key {devices}.")
            # TODO: Retry twice to look for key insertion:
            print("WARNING: fido2_secret() found no FIDO2 devices. Using fallback key generation.")
            fallback_key = generate_fallback_key()
            return fallback_key
        else:
            # Get the first device
            device = devices[0]
            # Extract a numeric identifier from the device
            # The device object has attributes like product_string, manufacturer_string, etc.
            # For now, let's use the hash of the device string representation as a numeric key
            device_str = str(device)
            # Extract the numeric part from the device string if it exists
            #import re
            numbers = re.findall(r'\d+', device_str)
            if numbers:
                number = int(numbers[0])  # Use the first number found
                print(f"SECRET: fido2_salted_secret(): number={str(number)} from FIDO2 devices.")
            else:
                # number = abs(hash(device_str)) % (10**8)  # Keep it to 8 digits max
                print(f"FATAL: fido2_salted_secret(): No numbers identified from \"{str(numbers)}\" ")
                # Fallback not generated here because the fallback is to use unencrypted file below.

        if not use_salt:    # use_salt = False
            # Generate a 32-byte key from the number (e.g., using SHA256)
            # and then base64 url-safe encode it for Fernet.
            # nounced32 = str(number) + "1123456789012345678"
            nounced32 = Fernet.generate_key()
            print(f"DEBUG: fido2_salted_secret(): nounced32 is {len(nounced32)} bytes! \"{nounced32}\" ")
            #raw_key = key.decode()  # This is a valid key string to store/use
            #print(f"DEBUG: fido2_salted_secret(): raw_key is {len(raw_key)} bytes! \"{str(raw_key)}\" ")
            #raw_key = hashlib.sha256(str(number).encode()).digest()
            raw_key = str(nounced32).encode()
            #print(f"DEBUG: fido2_salted_secret(): raw_key is {len(raw_key)} bytes! {str(raw_key)}")
            
            #FIXME:
            #key_bytes = base64.urlsafe_b64encode(raw_key)
            key_bytes = raw_key
            #print(f"DEBUG: fido2_secret(): Unsalted Fernet key (base64 encoded) has {len(key_bytes)} bytes!")
            return key_bytes
        else:
            nounced = str(number)
            print(f"DEBUG: fido2_salted_secret(): {len(nounced)} bytes!")

            # Based on https://thepythoncode.com/article/encrypt-decrypt-files-symmetric-python
            # import secrets
            salt = secrets.token_bytes(16)  # Generate new salt of size 16:
            print(f"DEBUG: fido2_salted_secret(): salt={salt}")

            # generate key from the salt and the password:
            # import Scrypt to salt password:
            kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
            # length: The desired length of the key (32 in this case).
            # n: CPU/Memory cost parameter, must be larger than 1 and be a power of 2.
            # r: Block size parameter.
            # p: Parallelization parameter.
            # kdf=<cryptography.hazmat.primitives.kdf.scrypt.Scrypt object at 0x105533190>
            # TECHNIQUE: Derive a key:
            derived_key = kdf.derive(nounced.encode())
            print(f"SECRET: fido2_salted_secret(): kdf={str(kdf)}")
            # encode it using Base 64 and return it
            key_bytes = base64.urlsafe_b64encode(derived_key)
            print(f"INFO: fido2_secret(): Salted Fernet key (base64 encoded) has {len(key_bytes)} bytes!")
            return key_bytes
        
    except Exception as e:
        print(f"ERROR: fido2_secret(): {e}")
        return None


def encrypt_file_gnupg(public_key_file, input_file, output_file):
    """Encrypt a file using a (GNU Privacy Guard) public key."""
    # import gnupg
    gpg = gnupg.GPG()
    # Import the public key:
    with open(public_key_file, 'r') as key_file:
        key_data = key_file.read()
        import_result = gpg.import_keys(key_data)

    # Encrypt the input file using the imported public key:
    with open(input_file, 'rb') as f:
        status = gpg.encrypt_file_gnupg(
            f,
            recipients=import_result.fingerprints,
            output=output_file,
            always_trust=True
        )
    if status.ok:
        print(f"encrypt_file_gnupg(): encrypted file {output_file}")
    else:
        print("encrypt_file_gnupg(): failed:", status.status)


def get_encrypt_key_obj(password=None) -> str:
    """Create symmetric key_obj using the Fernet library."""
    #from cryptography.fernet import Fernet
    key_obj = Fernet.generate_key()
    # Context manager to load the key for encryption/decryption:
    with open('key.key', 'wb') as key_file:
        key_file.write(key_obj)
    return key_obj


def encrypt_str(cleartext_str, key_obj) -> str:
    """Encrypt string with URL-safe 44-byte base64 AES-256 symmetric key using the Fernet library.
    
    Fernet tokens are base64-encoded and transport-safe. TODO: TTL expiry.
    """
    #from cryptography.fernet import Fernet
    # TODO: Verify key_obj is usable.
    # Create a cipher_suite object from Fernet object:
    cipher_suite = Fernet(key_obj)
    # TODO: Validate cleartext string to be encrypted:
    plain_text = cleartext_str
    # Encrypt text using cipher_suite:
    encrypted_text = cipher_suite.encrypt(plain_text.encode())
    # Fernet supports key rotation using MultiFernet to manage multiple keys and rotate secrets easily.
    return encrypted_text


def decrypt_str(encrypted_text, key_obj) -> str:
    """Decrypt text encrypted with symmetric AES-256 password using the Fernet library."""
    #from cryptography.fernet import Fernet
    cipher_suite = Fernet(key_obj)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text


def symmetrically_encrypt_file(filepath, key_str):
    """Encrypt file using a symmetric (two-way) key."""
    if not key_str:
        fido2_secret_key = fido2_secret()
        if not fido2_secret_key:
            print("WARNING: symmetrically_encrypt_file(): FIDO2 key not available!")
            return None
    else:
        #key = fido2_secret_key.encode()
        key = fido2_secret_key
        print(f"VERBOSE: symmetrically_encrypt_file(): base64 encoded Fernet key has {len(key_str)} bytes!")

    try:
        #from cryptography.fernet import Fernet, InvalidToken
        #from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
        fernet = Fernet(key)
        # Convert to string if filepath is a Path object:
        filepath_str = str(filepath) if hasattr(filepath, 'is_file') else filepath
        # Fernet requires read of file before encryption:
        with open(filepath_str, "rb") as file:
            file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
        with open(filepath_str, "wb") as file:
            file.write(encrypted_data)
        print(f"VERBOSE: symmetrically_encrypt_file(): contains {len(encrypted_data)} encrypted bytes!")
        return encrypted_data

    except Exception as e:
        print(f"ERROR: symmetrically_encrypt_file(): failed: {e}")
        return None


def symmetrically_decrypt_file(filepath, key_str) -> str:
    """Decrypt file using a symmetric (two-way) key."""
    print(f"VERBOSE: Fernet key (base64 encoded): has {len(str(key_str))} bytes!")
    #from cryptography.fernet import Fernet
    # instead of key = Fernet.generate_key()
    # key = str(key_str).encode()  # key = b'your_str_here' (normally 86 bytes?)
    key = key_str
    fernet = Fernet(key)

    # Convert to string if filepath is a Path object
    filepath_str = str(filepath) if hasattr(filepath, 'is_file') else filepath
    with open(filepath_str, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data

    except Exception as e:
        print(f"ERROR: symmetrically_decrypt_file() failed: {e}")
        return None


# TODO: def add/update entry in .env file encrypted/decrypted using FIDO2

def generate_fallback_key() -> bytes:
    """Generate a fallback encryption key when FIDO2 is not available.
    
    Uses a combination of system information to create a reproducible key.
    Note: This is less secure than FIDO2 but allows the program to function.
    """
    import platform
    import getpass
    
    # Combine system info to create a seed
    system_info = (
        platform.node() +  # hostname
        platform.system() +  # OS name
        getpass.getuser() +  # username
        "fallback_seed_2024"
    )
    
    # Create a 32-byte key from the system info
    raw_key = hashlib.sha256(system_info.encode('utf-8')).digest()
    key_bytes = base64.urlsafe_b64encode(raw_key)
    
    print(f"INFO: Generated fallback key (base64 encoded) with {len(key_bytes)} bytes.")
    return key_bytes


# def add_env_file(variable_name) -> bool:


def load_env_file(variable_name, filepath='~/python-samples.env.enc', decrypted_env_data=None) -> str:
    """Retrieve a variable from an .enc (encrypted .env file) decrypted into memory.
    
    USAGE: my_variable = load_env_file('VARIABLE_NAME','.enc_file_path')
    Instead of like: api_key = os.getenv("API_KEY") using
        settings = Dynaconf(settings_files=['settings.toml']); print(settings.database_url)
    TODO: Encrypt using a key in Titan USB serial number. Rename with .enc for encrypted.
    TODO: Add a parm to retrieve variable from cloud store (Pulumi/Akeyless/AWS Secret Manager, etc.)
    Titan is $35. FIDO is $60. https://onlykey.io is $49.99.
    enc_file_created = True
    """
    home_env_filepath = filepath_audit(filepath)

    if home_env_filepath[-4:] == ".env":    # it's NOT an encrypted file:
        # Just use the .env file directly
        pass
              
    elif home_env_filepath[-4:] == ".enc":    # it's an encrypted file, so try to decrypt
        # Check if we have FIDO2 devices available (not just fallback key)
        devices = list(CtapHidDevice.list_devices())
        if not devices:
            # No FIDO2 devices available, fall back to unencrypted .env file
            home_env_filepath = filepath_audit('~/python-samples.env')
            print(f"WARNING: No FIDO2 devices found. Falling back to unencrypted .env file: {home_env_filepath}")
        else:
            # We have FIDO2 devices, try to decrypt the .enc file
            fido2_secret_key = fido2_secret()
            print("DEBUG: load_env_file(): attempting to decrypt with FIDO2 key...")
            try:
                decrypted_env_data = symmetrically_decrypt_file(home_env_filepath, fido2_secret_key)
                if decrypted_env_data:
                    # Successfully decrypted, parse in memory
                    stream = StringIO(decrypted_env_data.decode('utf-8'))
                    config = dotenv_values(stream=stream)
                    if variable_name in config:
                        result = config[variable_name].strip('\"').strip('\'')
                        return result
                    else:
                        print(f"Variable '{variable_name}' not found in encrypted .env file")
                        return None
                else:
                    print("Failed to decrypt .env file, falling back to unencrypted version")
                    home_env_filepath = filepath_audit('~/python-samples.env')
            except Exception as e:
                print(f"Error decrypting .env file: {e}, falling back to unencrypted version")
                home_env_filepath = filepath_audit('~/python-samples.env')
        
    else:
        print(f"FATAL: load_env_file(): file {home_env_filepath} extension not recognized!")
        return None
    
    # At this point, home_env_filepath should point to the unencrypted .env file
    print(f"VERBOSE: Lookup variable \"{variable_name}\" from file {home_env_filepath}...")
    env_path = Path(home_env_filepath)
    
    if env_path.is_file() and env_path.exists():
        if SHOW_DEBUG:
            print(f"DEBUG: load_env_file(): file {env_path} is accessible")
        
        try:
            with open(env_path) as file:
                for line in file:
                    # Strip whitespace and ignore comments or empty lines:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    
                    # Split the line into key and value:
                    key_value = line.split('=', 1)
                    if len(key_value) != 2:
                        continue
                    
                    key, value = key_value
                    if key.strip() == variable_name:
                        result = value.strip().strip('\"').strip('\'')
                        return result
            print(f"Variable '{variable_name}' not found in .env file")
            return None
        except Exception as e:
            print(f"ERROR: load_env_file(): {e}")
            return None
    else:
        print(f"ERROR: load_env_file(): .env file {env_path} is not accessible")
        return None


if __name__ == '__main__':

    print(f"__last_change__ {__last_change__}")

    local_timestamp = gen_local_timestamp()
    if SHOW_DEBUG:
        pgm_strt_mem_used, pgm_process = pgm_memory_used()
        print(f"DEBUG: {pgm_process}")
        print("DEBUG: pgm_memory used()="+str(pgm_strt_mem_used)+" MiB being used.")
        pgm_strt_disk_free = pgm_diskspace_free()
        print(f"DEBUG: pgm_diskspace_free()={pgm_strt_disk_free:.2f} GB")
        # list_disk_space_by_device()

    #pulumi_region = load_env_file("PULUMI_REGION",'~/python-samples.env.enc')
    pulumi_region = load_env_file("PULUMI_REGION")
    if pulumi_region:
        print(f"INFO: pulumi_region={pulumi_region}")

    pgm_has_fda = pgm_fda_test()
    # Manually set 

    filepath="~/github-wilsonmar/python-samples/"
    dir_size = dir_raw_size(filepath)
    print(f"INFO: {format_bytes(dir_size)} in {filepath}")
        # INFO: 9.86MiB=10.34MB in data/movies.json

    print("\nFile byte size:")
    filepath = "data/movies.json"
    file_size = file_raw_size(filepath)
    print(f"INFO: {format_bytes(file_size)} in {filepath}")
        # INFO: 9.86MiB=10.34MB in data/movies.json

    print("\nRandom Numbers:")
    random_num(19,"random")  # (number of digits, algorithm)
    random_num(19,"urandom")  # (number of digits, algorithm)
    random_num(19,"randbelow")  # (number of digits, algorithm)
    random_num(19,"randbits")  # (number of digits, algorithm)


    with open(filepath, "rb") as file:
        file_data = file.read()
    entropy_value = shannon_entropy(file_data)
    print(f"Entropy of file '{filepath}': {entropy_value:.4f} bits per byte")
    # https://cocomelonc.github.io/malware/2022/11/05/malware-analysis-6.html This function reads the file in binary mode, counts the frequency of each byte, then calculates the entropy by summing the probabilities times their log base 2, yielding an entropy value in bits per byte. Higher entropy indicates more randomness (e.g., encrypted or compressed files). Typical entropy values range from 0 (all bytes the same) to 8 (completely random).x  

    print("\nUUID:")
    uuid_rand = gen_uuid_rand()
    print(f"INFO: UUIDv4 Random :     {uuid_rand}")
    uuid_seq = gen_uuid_seq()
    print(f"INFO: UUIDv1 Sequential : {uuid_seq}")


    print("\nHashing:")

    hash_type = "SHA256"
    hash = hash_txt(cleartext, hash_type)
    print(f"{hash_type} => {len(hash)} char.  {hash}")

    hash_type = "ARGON2ID"
    hash = hash_txt(cleartext, hash_type)
    print(f"{hash_type} => {len(hash)} char. {hash}")

    hash_type = "SHA512"
    hash = hash_txt(cleartext, hash_type)
    print(f"{hash_type} => {len(hash)} char. {hash}")

    hash_type = "MD5"
    hash = hash_txt(cleartext, hash_type)
    print(f"{hash_type}    => {len(hash)} char.  {hash}")


    print("\nEnryption/Decryption check (text not shown to maintain privacy):")
    key_obj = get_encrypt_key_obj()
    encrypted_text = encrypt_str(cleartext, key_obj)
    print(f"Encrypted: {len(encrypted_text)} chars")

    decrypted_text = decrypt_str(encrypted_text, key_obj)
    # CAUTION: Do not print out encrypted text to console!
    print(f"Decrypted: {len(encrypted_text)} chars ")
    if decrypted_text == cleartext:
        print("VERBOSE: Encrypted text matches decrypted text!")
    else:
        print("FATAL: Encrypted text does not match decrypted text!")
    

    print("\nFIXME: gnuPG not installed?")
    exit(9)
    filepath = "file_to_encrypt.txt"
    # FIXME: RuntimeError: GnuPG is not installed!
    encrypt_file_gnupg('recipient_public_key.asc', filepath, 'encrypted_output.gpg')

    
    if SHOW_SUMMARY:
        loops_count = 0
        pgm_summary(pgm_strt_datetimestamp, loops_count)

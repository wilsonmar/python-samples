#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

__commit_date__ = "2025-06-19"
__commit_msg__ = "v002 + update meta output :fido2-titan.py"
__repository__ = "https://github.com/wilsonmar/python-samples/blob/main/fido2-titan.py"
__status__ = "WORKS until authentication."

"""fido2-titan.py
This uses the FIDO2/WebAuthn protocol to find and read a 
FIDO2-compliant Yubikey OTP+FIDO+CCID key or 
$35 https://cloud.google.com/security/products/titan-security-key
REMEMBER: Touch the key when it blinks during operations
CLI:
    uv pip install fido2   # or in requirements.txt
Key Features:
* TASK 1 - Auto-detection: Automatically finds key plugged in
* TASK 2 - Comprehensive info: Shows all available device capabilities
* TASK 3 - Full workflow: Tests both registration and authentication
* Error handling: Graceful handling of common issues
"""
# Based on Claude AI prompt
import sys
import os

try:
    from fido2.hid import CtapHidDevice
    from fido2.client import Fido2Client
    from fido2.server import Fido2Server
    from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity
    from fido2 import cbor
except Exception as e:
    print(f"Python module import failed: {e}")
    #print("    sys.prefix      = ", sys.prefix)
    #print("    sys.base_prefix = ", sys.base_prefix)
    print(f"Please activate your virtual environment:\n  python3 -m venv venv\n  source venv/bin/activate\n  pip install ...")
    exit(9)


def get_client_data_collector():
    """Create a simple client data collector for FIDO2Client"""
    def collector(origin):
        # Create basic client data
        client_data = ClientData(
            type="webauthn.create",  # or "webauthn.get" for authentication
            origin=origin,
            challenge=b"dummy_challenge"
        )
        return CollectedClientData(client_data)
    return collector

def find_fido2_devices():
    """Find and list all FIDO2 devices"""
    print("TASK 1 - Find FIDO2 devices")
    
    try:
        # Find all CTAP HID devices
        devices = list(CtapHidDevice.list_devices())
        print(f"Found {len(devices)} FIDO2 device(s):")
        
        if not devices:
            print("  No FIDO2 devices found.")
            return []
        
        for i, device in enumerate(devices, 1):
            print(f"  Device {i}: {device}")
            
        return devices
    
    except Exception as e:
        print(f"Error finding devices: {e}")
        return []


def read_device_info(devices):
    """Read information from FIDO2 devices"""
    print("\nTASK 2 - Read device information:")
    
    if not devices:
        print("No devices to read from.")
        return
    
    for i, device in enumerate(devices, 1):
        try:
            print(f"\n--- Device {i} ---")
            
            # Create FIDO2 client with proper client_data_collector:
            client_data_collector = get_client_data_collector()
            client = Fido2Client(device, "https://example.com", client_data_collector)
            
            # Get device info
            info = client.info
            print(f"FIDO2 Client Info: {info}")
            
            # Try to get CTAP info if available
            if hasattr(device, 'ctap'):
                ctap = device.ctap
                if hasattr(ctap, 'info'):
                    ctap_info = ctap.info
                    print(f"CTAP Info: {ctap_info}")
                    
                    # Print specific details if available
                    if hasattr(ctap_info, 'versions'):
                        print(f"  Supported versions: {ctap_info.versions}")
                    if hasattr(ctap_info, 'aaguid'):
                        print(f"  AAGUID: {ctap_info.aaguid.hex()}")
                    if hasattr(ctap_info, 'max_msg_size'):
                        print(f"  Max message size: {ctap_info.max_msg_size}")
                    if hasattr(ctap_info, 'pin_uv_auth_protocols'):
                        print(f"  PIN/UV auth protocols: {ctap_info.pin_uv_auth_protocols}")
                    if hasattr(ctap_info, 'options'):
                        print(f"  Options: {dict(ctap_info.options)}")
            
            # Device descriptor info
            descriptor = device.descriptor
            if hasattr(descriptor, 'path'):
                print(f"Device path: {descriptor.path}")
            if hasattr(descriptor, 'pid'):
                print(f"Product ID: 0x{descriptor.pid:04x}")
            if hasattr(descriptor, 'vid'):
                print(f"Vendor ID: 0x{descriptor.vid:04x}")
            if hasattr(descriptor, 'product_name') and descriptor.product_name:
                print(f"Product: {descriptor.product_name}")
            if hasattr(descriptor, 'serial_number') and descriptor.serial_number:
                print(f"Serial Number: {descriptor.serial_number}")
            if hasattr(descriptor, 'report_size_in'):
                print(f"Report size in: {descriptor.report_size_in}")
            if hasattr(descriptor, 'report_size_out'):
                print(f"Report size out: {descriptor.report_size_out}")
                
        except Exception as e:
            print(f"Error reading device {i} info: {e}")


def test_authentication(device):
    """Test basic authentication with the Titan key"""
    try:
        # Create FIDO2 client with proper client_data_collector:
        client_data_collector = get_client_data_collector()
        client = Fido2Client(device, client_data_collector)
        print(f"client={client}")
     
        # Create a test server:
        rp = PublicKeyCredentialRpEntity("example.com", "Example Corp")
        server = Fido2Server(rp)
        
        # Create a test user
        user = PublicKeyCredentialUserEntity(
            id=b"user_id_123",
            name="testuser@example.com",
            display_name="Test User"
        )
        
        print("Testing credential creation (registration)...")
        print("Please touch your Titan key when it blinks...")
        
        # Create credential
        create_options, state = server.register_begin(
            user,
            resident_key_requirement="discouraged"
        )
        
        result = client.make_credential(create_options["publicKey"])
        
        # Complete registration
        auth_data = server.register_complete(state, result)
        credential_id = auth_data.credential_data.credential_id
        
        print("✓ Registration successful!")
        print(f"  Credential ID: {credential_id.hex()}")
        print(f"  Public key algorithm: {auth_data.credential_data.public_key_algorithm}")
        
        # Test authentication
        print("\nTesting authentication...")
        print("Please touch your Titan key when it blinks...")
        
        request_options, state = server.authenticate_begin([credential_id])
        assertion = client.get_assertion(request_options["publicKey"])
        
        server.authenticate_complete(state, assertion.get_response(0))
        
        print("✓ Authentication successful!")
        return True
        
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        # FIXME: Fido2Client.__init__() missing 1 required positional argument: 'client_data_collector'
        return False


def main():
    """Main function to demonstrate FIDO2 device detection and info reading"""

    import inspect
    print(f"{inspect.getfile(inspect.currentframe())}: FIDO2/Google Titan Reader")

    # Find devices:
    devices = find_fido2_devices()
    if devices:
        # Read device information:
        read_device_info(devices)

        # TODO: Read parameter -device instead of the first device found:
        device = devices[0]
        print(f"\nTASK 3 - Authenticate {device}:")
        #if test_authentication(device):
        #    print("All tests passed! Your Titan key is working properly.")
        #else:
        #    print("Some tests failed. Check your key connection and try again.")

if __name__ == "__main__":
    main()

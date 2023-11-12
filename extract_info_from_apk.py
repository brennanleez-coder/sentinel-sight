import re
import subprocess

def extract_version_code(output):
    match = re.search(r"versionCode='(\d+)'", output)
    return match.group(1) if match else None

def extract_version_name(output):
    match = re.search(r"versionName='([^']+)'", output)
    return match.group(1) if match else None

def extract_package_name(output):
    match = re.search(r"package: name='([^']+)'", output)
    return match.group(1) if match else None

def extract_app_cert_hash(output):
    '''
    Output from apksigner:
    Signer #1 certificate DN: CN=Facebook Corporation, OU=Facebook, O=Facebook Mobile, L=Palo Alto, ST=CA, C=US
    Signer #1 certificate SHA-256 digest: e3f9e1e0cf99d0e56a055ba65e241b3399f7cea524326b0cdd6ec1327ed0fdc1
    Signer #1 certificate SHA-1 digest: 8a3c4b262d721acd49a4bf97d5213199c86fa2b9
    Signer #1 certificate MD5 digest: 3fad024f2dcbe3ee693c96f350f8e376
    '''
    
    match = re.search(r"Signer #1 certificate SHA-256 digest: ([a-f0-9]+)", output)
    
    return match.group(1) if match else None


def extract_info(directory_of_aapt, apk_file_path):
    command = ["aapt", "dump", "badging", apk_file_path]
    # Run aapt to get the version info
    result = subprocess.run(command, cwd=directory_of_aapt, stdout=subprocess.PIPE)
    output = result.stdout.decode()
    version_code = extract_version_code(output)
    version_name = extract_version_name(output)
    package_name = extract_package_name(output)
    
    command = ["apksigner", "verify", "--print-certs", apk_file_path]
    result = subprocess.run(command, cwd=directory_of_aapt, stdout=subprocess.PIPE)
    output = result.stdout.decode()
    app_cert_hash = extract_app_cert_hash(output)

    # Return the info as JSON
    output = {
        'version_code': version_code,
        'version_name': version_name,
        'package_name': package_name,
        'app_cert_hash': app_cert_hash
    }
    return output
    
# test extract_info
directory_of_aapt = '/Users/brennanlee/library/Android/sdk/build-tools/33.0.1/'
apk_file_path = '/Users/brennanlee/Desktop/extractedApks/Facebook_441.0.0.0.93_apkcombo.com.apk'

# if does not run, add aapt and apksigner to PATH
# Location of tools: /Users/brennanlee/library/Android/sdk/build-tools/33.0.1

print(extract_info(directory_of_aapt, apk_file_path))
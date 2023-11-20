import re
import subprocess
from hash_util import compute_sha256_from_apk

def extract_version_code(aapt_output):
    match = re.search(r"versionCode='(\d+)'", aapt_output)
    return match.group(1) if match else None

def extract_version_name(aapt_output):
    match = re.search(r"versionName='([^']+)'", aapt_output)
    return match.group(1) if match else None

def extract_package_name(aapt_output):
    match = re.search(r"package: name='([^']+)'", aapt_output)
    return match.group(1) if match else None
def extract_permissions(aapt_output):
    permissions = re.findall(r'uses-permission: name=\'([^\']+)\'', aapt_output)
    return ', '.join(permissions) if permissions else None

def extract_apk_hash(apk_file_path):
    '''
    apk_file_path: path to the apk file
    '''
    return compute_sha256_from_apk(apk_file_path) if apk_file_path else None


def extract_app_cert_hash(apksigner_output):
    '''
    apksigner_output:
    Signer #1 certificate DN: CN=Facebook Corporation, OU=Facebook, O=Facebook Mobile, L=Palo Alto, ST=CA, C=US
    Signer #1 certificate SHA-256 digest: e3f9e1e0cf99d0e56a055ba65e241b3399f7cea524326b0cdd6ec1327ed0fdc1
    Signer #1 certificate SHA-1 digest: 8a3c4b262d721acd49a4bf97d5213199c86fa2b9
    Signer #1 certificate MD5 digest: 3fad024f2dcbe3ee693c96f350f8e376
    '''
    
    match = re.search(r"Signer #1 certificate SHA-256 digest: ([a-f0-9]+)", apksigner_output)
    
    return match.group(1) if match else ""


# params: directory of tools, apk file path
# directory of tools is the location of aapt and apksigner
# apk_file_path is the location of the apk file
# return: json object of the extracted info
def extract_info(directory_of_tools, apk_file_path):
    aapt_command = ["aapt", "dump", "badging", apk_file_path]
    # Run aapt to get the version info
    aapt_result = subprocess.run(aapt_command, cwd=directory_of_tools, stdout=subprocess.PIPE)
    aapt_output = aapt_result.stdout.decode()
    version_code = extract_version_code(aapt_output)
    version_name = extract_version_name(aapt_output)
    package_name = extract_package_name(aapt_output)
    permissions = extract_permissions(aapt_output)
    app_hash = extract_apk_hash(apk_file_path)
    
    # run apksigner to get the app cert hash
    # apksigner_command = ["apksigner", "verify", "--print-certs", apk_file_path]
    # apksigner_result = subprocess.run(apksigner_command, cwd=directory_of_tools, stdout=subprocess.PIPE)
    # apksigner_output = apksigner_result.stdout.decode()
    app_cert_hash = extract_app_cert_hash(aapt_output)

    # Return the info as JSON
    output = {
        'version_code': version_code,
        'version_name': version_name,
        'package_name': package_name,
        'app_cert_hash': app_cert_hash,
        'app_hash': app_hash,
        'permissions': permissions,
    }
    return output
    
# Mac
# test extract_info
# directory_of_tools = '/Users/brennanlee/library/Android/sdk/build-tools/33.0.1/'
# apk_file_path = '/Users/brennanlee/Desktop/extractedApks/Facebook_441.0.0.0.93_apkcombo.com.apk'
# If does not run, add aapt and apksigner to PATH
# Location of tools: /Users/brennanlee/library/Android/sdk/build-tools/33.0.1
# export PATH=$PATH:/Users/brennanlee/library/Android/sdk/build-tools/33.0.1


# Windows
directory_of_tools = "C:\\Users\\Cyber\\AppData\\Local\\Android\\Sdk\\build-tools\\33.0.1\\"
apk_file_path = "C:\\Users\\Cyber\\Desktop\\extractedApks\\base.apk"



# print(extract_info(directory_of_tools, apk_file_path))
# directory_of_local_apks = "C:\\Users\\Cyber\\Desktop\\extractedApks\\"
# for filename in os.listdir(directory_of_local_apks):
#         if filename.endswith(".apk"):

#             apk_path = os.path.join(directory_of_local_apks, filename)
#             print(extract_info(directory_of_tools, apk_path))
#             print('\n')

#             # command = ["aapt", "dump", "badging", apk_path]
#             # result = subprocess.run(command, cwd=directory_of_tools, stdout=subprocess.PIPE)

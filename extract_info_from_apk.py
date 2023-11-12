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


def extract_info(directory_of_aapt, apk_file_path):

    command = ["aapt", "dump", "badging", apk_file_path]
    # Run aapt to get the version info
    result = subprocess.run(command, cwd=directory_of_aapt, stdout=subprocess.PIPE)
    
    output = result.stdout.decode()

    version_code = extract_version_code(output)
    version_name = extract_version_name(output)
    package_name = extract_package_name(output)

    # Return the info as JSON
    output = {
        'version_code': version_code,
        'version_name': version_name,
        'package_name': package_name
    }
    return output
    
# test extract_info
directory_of_aapt = '/Users/brennanlee/library/Android/sdk/build-tools/33.0.1/'
apk_file_path = '/Users/brennanlee/Desktop/extractedApks/Facebook_441.0.0.0.93_apkcombo.com.apk'
# if does not run, add aapt to PATH
print(extract_info(directory_of_aapt, apk_file_path))
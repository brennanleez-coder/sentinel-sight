import subprocess
import re

from apkutils import APK

# Path to your APK file
apk_path = '../extractedApks/base.apk'

# Function to run aapt and extract the version code and name
def get_apk_info(apk_path):
    try:
        # Run aapt to get the badging information
        result = subprocess.run(['aapt', 'dump', 'badging', apk_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if aapt command was successful
        if result.returncode != 0:
            print("aapt failed to run:", result.stderr)
            return None
        
        # Process output
        output = result.stdout
        version_code = extract_version_code(output)
        version_name = extract_version_name(output)
        
        return version_code, version_name
    except Exception as e:
        print("An error occurred:", e)
        return None

# Function to extract the version code
def extract_version_code(output):
    match = re.search(r"versionCode='(\d+)'", output)
    return match.group(1) if match else "Unknown"

# Function to extract the version name
def extract_version_name(output):
    match = re.search(r"versionName='([^']+)'", output)
    return match.group(1) if match else "Unknown"

# Run the script
if __name__ == '__main__':
    version_info = get_apk_info(apk_path)
    if version_info:
        version_code, version_name = version_info
        print(f"Version Code: {version_code}")
        print(f"Version Name: {version_name}")

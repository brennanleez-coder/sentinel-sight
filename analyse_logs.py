# Define the function to analyze the provided text
def analyze_log_text(text):
    # Dictionary to hold the count of each phrase
    phrases_mapping = {
        # "APK Received": "Total APK Received",
        # "awaiting downloaded APK": "Awaiting Downloaded APK",
        # "APK check": "Total APK Checked",
    }

    phrases_to_count = {
        # "Total APK Received": 0,
        # "Awaiting Downloaded APK": 0,
        # "Total APK Checked": 0,
    }
    # Initialize reconciliation count
    reconciliation_count = {}

    # Split the text into lines and iterate over them
    for line in text.split('\n'):
        # Check for each phrase and count occurrences
        for phrase in phrases_mapping.keys():
            if phrase in line:
                phrases_to_count[phrases_mapping[phrase]] += 1

        # Check for reconciliation pattern and count occurrences
        if "Rank" in line:
            # Extract the rank number
            rank_number = line.split('Rank')[1].split('-')[0].strip()
            # Count occurrences of each rank number
            if rank_number not in reconciliation_count:
                reconciliation_count[rank_number] = 0
            reconciliation_count[rank_number] += 1

    return phrases_to_count, reconciliation_count

# Example usage:
log_text = """
Monitoring started...
Socket open...
Listener triggered...
2023_12_06 11_43_01 - No files to move.
2023_12_06 11_43_01 - Processing downloaded apks...
2023_12_06 11_43_04 - legit_apk_info table is up to date.
2023_12_06 11_43_04 ===================================== 
Processing retrieved apk...

2023_12_06 11_43_04 ============APK Received============= 
package_name: TEST PACKAGE NAME
version_name: 1.0
version_code: 1
apk_hash: TEST INCOMING APK HASH
app_cert_hash: TEST INCOMING APP CERT HASH
permissions: TEST INCOMING PERMISSIONS

2023_12_06 11_43_04 - No files to move.
2023_12_06 11_43_04 - Processing downloaded apks...
Processing retrieved apk...

2023_12_06 11_43_05 ============APK Received============= 
package_name: TEST PACKAGE NAME
version_name: 1.0
version_code: 1
apk_hash: TEST INCOMING APK HASH
app_cert_hash: TEST INCOMING APP CERT HASH
permissions: TEST INCOMING PERMISSIONS

2023_12_06 11_43_05 - No files to move.
2023_12_06 11_43_05 - Processing downloaded apks...
2023_12_06 11_43_07 - legit_apk_info table is up to date.
2023_12_06 11_43_07 ===================================== 
2023_12_06 11_43_07 ===================================== 
2023_12_06 11_43_07 - TEST PACKAGE NAME: version code: 1 awaiting downloaded APK.
2023_12_06 11_43_07 ===================================== 
2023_12_06 11_43_08 - legit_apk_info table is up to date.
2023_12_06 11_43_08 ===================================== 
2023_12_06 11_43_08 ===================================== 
2023_12_06 11_43_08 - TEST PACKAGE NAME: version code: 1 PENDING APK CHECKS.
2023_12_06 11_43_08 ===================================== 
Processing retrieved apk...

2023_12_06 11_45_27 ============APK Received============= 
package_name: com.example.myapplication
version_name: 1.0
version_code: 1
apk_hash: 650baa27ef31754216f38ada8d2b19841effcf998add35a045c3ade99a93f215
app_cert_hash: 7f48c4ae8c4bff0154cb6aa02f6e6d3341979f8fa757a6aae929ed22778ad222
permissions:

2023_12_06 11_45_27 - No files to move.
2023_12_06 11_45_27 - Processing downloaded apks...
2023_12_06 11_45_30 - legit_apk_info table is up to date.
2023_12_06 11_45_30 ===================================== 
2023_12_06 11_45_30 ===================================== 
2023_12_06 11_45_31 - com.example.myapplication: version code: 1 PENDING APK CHECKS.
2023_12_06 11_45_31 ===================================== 
2023_12_06 11_45_31 ============APK Result============= 
2023_12_06 11_45_31 - com.example.myapplication: 1 legitimacy: Rank 2 - DIFF: Permissions |Same: App Cert Hash, App Hash.
2023_12_06 11_45_31 =================================== 
2023_12_06 11_48_04 - No files to move.
2023_12_06 11_48_04 - Processing downloaded apks...
2023_12_06 11_48_07 - legit_apk_info table is up to date.
2023_12_06 11_48_07 ===================================== 
2023_12_06 11_53_07 - No files to move.
2023_12_06 11_53_07 - Processing downloaded apks...
2023_12_06 11_53_10 - legit_apk_info table is up to date.
2023_12_06 11_53_10 ===================================== 
2023_12_06 11_58_10 - No files to move.
2023_12_06 11_58_10 - Processing downloaded apks...
2023_12_06 11_58_13 - legit_apk_info table is up to date.
2023_12_06 11_58_13 ===================================== 
"""

# phrases_count, reconciliation_count = analyze_log_text(log_text)
# print("Phrases Count:", phrases_count)
# print("Reconciliation Count:", reconciliation_count)

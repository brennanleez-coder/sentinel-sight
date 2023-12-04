from enum import Enum

class HashResult(Enum):
    
    PENDING="PENDING: downloaded apk"
    PASSED="Rank 1: PASSED - Same: App Hash, App Cert Hash, Permissions"
    DIFF_PSACHAH="Rank 2 - DIFF: Permissions |Same: App Cert Hash, App Hash"
    DIFF_ACHAHSP="Rank 3 - DIFF: App Cert Hash, App Hash | Same: Permissions"
    DIFF_PAHSACH="Rank 4 - DIFF: Permissions, App Hash | Same: App Cert Hash"
    DIFF_PACHSAH="Rank 5 - DIFF: Permissions, App Cert Hash | Same: App Hash"
    DIFF_AHPSACH="Rank 6 - DIFF: Permissions, App Hash | Same: App Cert Hash"
    DIFF_ACHPAH="Rank 7 - DIFF: App Cert Hash, App Hash, Permissions"

def determine_apk_legitimacy(incoming_apk_hash, downloaded_apk_hash, incoming_app_cert_hash, downloaded_app_cert_hash, incoming_permissions, downloaded_permissions):
    # Using hash_results enum, determine level of apk legitimacy
    # and update hash_checks_table result field
    is_same_app_hash = incoming_apk_hash == downloaded_apk_hash
    is_same_app_cert_hash = incoming_app_cert_hash == downloaded_app_cert_hash
    is_same_permissions = incoming_permissions == downloaded_permissions
    
    if is_same_app_hash and is_same_app_cert_hash and is_same_permissions:
        return HashResult.PASSED.value
    elif not is_same_permissions and is_same_app_cert_hash and is_same_app_hash:
        return HashResult.DIFF_PSACHAH.value
    elif not is_same_app_cert_hash and is_same_app_hash and is_same_permissions:
        return HashResult.DIFF_ACHAHSP.value
    elif not is_same_permissions and is_same_app_hash:
        return HashResult.DIFF_PAHSACH.value
    elif not is_same_permissions and is_same_app_cert_hash:
        return HashResult.DIFF_PACHSAH.value
    elif not is_same_app_hash and is_same_permissions:
        return HashResult.DIFF_AHPSACH.value
    else:
        return HashResult.DIFF_ACHPAH.value
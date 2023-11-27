from enum import Enum

class HashResult(Enum):
    
    PENDING="PENDING: downloaded apk"
    PASSED="PASSED - Same: App Hash, App Cert Hash, Permissions"
    DIFF_PSACHSAH="CHECKED - DIFF: Permissions, Same: App Cert Hash, App Hash"
    DIFF_ACHSAHP="CHECKED - DIFF:App Cert Hash, Same: App Hash, Permissions"
    DIFF_AHSACHP="CHECKED - DIFF:App Hash, Same: App Cert Hash, Permissions"
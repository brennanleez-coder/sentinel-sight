from enum import Enum

class HashResult(Enum):
    
    PENDING="PENDING: downloaded apk"
    PASSED="Rank 1: PASSED - Same: App Hash, App Cert Hash, Permissions"
    DIFF_PSACHAH="Rank 2: CHECKED - DIFF: Permissions, Same: App Cert Hash, App Hash"
    DIFF_PSACHP="Rank 3: CHECKED - DIFF: Permissions, Same: App Cert Hash, App Hash"
    DIFF_ACHAHSP="Rank 4: CHECKED - DIFF: App Cert Hash, App Hash, Same: Permissions"
    DIFF_PAHSACH="Rank 5: CHECKED - DIFF: Permissions, App Hash, Same: App Cert Hash"
    DIFF_PACHSAH="Rank 6: CHECKED - DIFF: Permissions, App Cert Hash, Same: App Hash"
    DIFF_AHPSACH="Rank 7: CHECKED - DIFF: Permissions, App Hash, Same: App Cert Hash"
    DIFF_ACHPAH="Rank 8: CHECKED - DIFF: App Cert Hash, App Hash, Permissions"

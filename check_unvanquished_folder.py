import os
import sys

def check_unvanquished_folder():
    if sys.platform == "win32":
        unvanquished_folder = os.path.join(os.environ["USERPROFILE"], "Documents", "My Games", "Unvanquished")
        if not os.path.exists(unvanquished_folder):
            return None
        return unvanquished_folder
    elif sys.platform == "linux":
        unvanquished_folder = os.path.join(os.environ["HOME"], ".local", "share", "unvanquished")
        if not os.path.exists(unvanquished_folder):
            unvanquished_folder = os.path.join(os.environ["HOME"], ".var", "app", "net.unvanquished.Unvanquished", "data", "unvanquished")
            if not os.path.exists(unvanquished_folder):
                return None
        return unvanquished_folder
    elif sys.platform == "darwin":
        unvanquished_folder = os.path.join(os.environ["HOME"], "Library", "Application Support", "Unvanquished")
        if not os.path.exists(unvanquished_folder):
            return None
        return unvanquished_folder
    else:
        return None
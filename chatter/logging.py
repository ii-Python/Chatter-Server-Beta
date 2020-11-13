# Modules
import sys
from datetime import datetime

# Main function
def verbose(*args):

    if "-v" in sys.argv:

        time = datetime.now().strftime("%D %H:%M:%S")
        time = f"[{time}]:"

        print(time, *args)

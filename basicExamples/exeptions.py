import sys
import os
PATH = 1

try:
    directory = sys.argv[PATH]
    print(os.listdir(directory))
except IndexError:
    print("Missing script parameter")
except WindowsError:
    print("No such directory")
except Exception as e:
    print("Error: {}".format(e))
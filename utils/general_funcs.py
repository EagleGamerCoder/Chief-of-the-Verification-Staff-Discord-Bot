'''

info 

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import random
import string

# Modules


# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# Generates a six digit code
def generate_code_six() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
'''

Info about module

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports


# Modules


# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

class BotContext:
    def __init__(self, db, log_error, create_server_rules_embed, create_verification_embed, VerifyView):
        self.db = db
        self.log_error = log_error
        self.create_server_rules_embed = create_server_rules_embed
        self.create_verification_embed = create_verification_embed
        self.VerifyView = VerifyView
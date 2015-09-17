__author__ = 'Trevor "Autogen" Grant'

from angemilner.key_librarian import APIKeyLibrarian

a = APIKeyLibrarian()

a.new_api_key("abc123", "tester", 5, 5)
a.check_out_api_key("tester")
a.summary()
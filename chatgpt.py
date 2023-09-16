import os
import sys

import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

query = sys.argv[1]
print(query)
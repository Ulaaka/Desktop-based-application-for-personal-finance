from FILE_handling import file_handling
from BASE_Classes import cryptography
from queries import query_processor
from system_functions import system_functions
query = query_processor()
system = system_functions()
df = query.get_transactions(1)
system.create_pdf('ulaaka', df)
#system.create_csv("ulaaka_file", df)
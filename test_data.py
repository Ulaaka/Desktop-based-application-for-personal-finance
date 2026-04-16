from file_handle import FileHandling
from base_classes import CryptoHelper
from db_queries import QueryProcessor
from system_functions import SystemHelpers
query = QueryProcessor()
system = SystemHelpers()
result = query.find_min_max(17, 'amount')

#result1 = query.total_transfer_or_extreme_value(1, 1, transfer_toggle=True, max_toggle=True, date_lower="2025-12-20", date_upper="2026-01-16")
result = query.common_transactions(1, 5, 1, True, "2025-08-20", "2026-01-16")
print(result)
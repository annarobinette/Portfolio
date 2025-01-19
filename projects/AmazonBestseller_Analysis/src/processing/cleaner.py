"""
Data cleaning functions for Amazon bestseller analysis.
Created on: 2025-01-17

Functions included:
- clean_title: Standardize book titles
- extract_series_info: Extract series name and number
- infer_format: Determine book format from available data
- standardize_age_range: Create consistent age ranges
"""
import re
import pandas as pd
from datetime import datetime



clean_title = <code object clean_title at 0x12b1aa700, file "/var/folders/11/kxlf585x3sx77xpyt3j79cbh0000gn/T/ipykernel_29948/3905757617.py", line 1>
clean_title.__doc__ = """Clean and standardize book titles"""

extract_series_info = <code object extract_series_info at 0x12b731160, file "/var/folders/11/kxlf585x3sx77xpyt3j79cbh0000gn/T/ipykernel_29948/3905757617.py", line 17>
extract_series_info.__doc__ = """Extract series name and book number if present"""

infer_format = <code object infer_format at 0x12b7508f0, file "/var/folders/11/kxlf585x3sx77xpyt3j79cbh0000gn/T/ipykernel_29948/925614636.py", line 1>
infer_format.__doc__ = """Infer format from title and price if format is missing"""

standardize_age_range = <code object standardize_age_range at 0x12b6ad450, file "/var/folders/11/kxlf585x3sx77xpyt3j79cbh0000gn/T/ipykernel_29948/1506147950.py", line 1>
standardize_age_range.__doc__ = """Create standardized age ranges based on category"""
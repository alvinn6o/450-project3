
'''
Data handling for tables to get the correct sheet and load the table as a df
'''

import pandas as pd

COLLAPSED_FILE = "Collapsed Patterns (Group).xlsx"
EXPANDED_FILE = "Expanded Patterns (Group).xlsx"

# Succesful is mispelled in original files
GROUP_LABELS = {
    "successful": "Succesful",
    "unsuccessful": "Unsuccesful",
}

AOI = ["A", "B", "C", "D", "E", "F", "G", "H"]
AOI_ENUMERATED = {aoi: i for i, aoi in enumerate(AOI)}



def get_sheet_name(group_key: str, exclude_a: bool) -> str:
    """
    Map (group, include/exclude A) to the correct Excel sheet name.
    Get the sheet name depending on filter
    Can exclude or include AOI A
    """
    base = GROUP_LABELS[group_key]
    if exclude_a:
        return f"{base} Excluding No AOI(A)"
    return base


def load_table(pattern_type: str, group_key: str, exclude_a: bool) -> pd.DataFrame:
    sheet_name = get_sheet_name(group_key, exclude_a)
    path = COLLAPSED_FILE if pattern_type == "collapsed" else EXPANDED_FILE

    df = pd.read_excel(path, sheet_name=sheet_name)
    
    return df

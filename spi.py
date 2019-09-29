__version__ = "v20190928"

import json


def Special_Instructions_Processing(QTY, str):
    if(str == False):
        return 0, 0
    # Remove Unwanted Characters
    str = str.replace('"', " ").replace('-', " ").replace('.',
                                                          " ").replace('th ', " ").replace(', ', " ").lower()
    # https://stackoverflow.com/a/4289557
    # Separate Integers From Strings
    Numbers = [int(s) for s in str.split() if s.isdigit()]

    # Determine Correct Output for QTY and CPS
    if(len(Numbers) != 0):
        if(QTY == min(Numbers) * max(Numbers)):
            return min(Numbers), max(Numbers)
        if(QTY == min(Numbers) == max(Numbers)):
            return 1, max(Numbers)
        if(min(Numbers) == max(Numbers)):
            if("every" in str or "each" in str or "into" in str or "between" in str):
                if(QTY % min(Numbers) == 0):
                    return int(QTY / min(Numbers)), min(Numbers)
                else:
                    return 0, 1
            if("complete" in str or "set" in str):
                return 0, min(Numbers)
        if("set" in str or "slip" in str or "page" in str or "sort" in str or "group" in str):
            return 0, 1
        return 0, 0
    else:
        return 0, 0


def Special_Instructions(JOB_INFO):
   # Get Information from JSON file, QTY, Comment Line #1 & #2
   # Process the information from both comment sections
    QTY = int(JOB_INFO.get('Copies', False))
    SPIO = Special_Instructions_Processing(
        QTY, JOB_INFO.get('Special Instructions', False))
    SLIO = Special_Instructions_Processing(
        QTY, JOB_INFO.get('Slip Sheets / Shrink Wrap', False))

    # Output States
    if(SPIO == (0, 1)):
        return 0, 0
    if(SLIO == (0, 1)):
        return 0, 0
    if (SPIO == SLIO == (0, 0)):
        return 1, QTY
    if (SPIO == SLIO):
        return SPIO
    if(SPIO == (0, 0)):
        return SLIO
    if(SLIO == (0, 0)):
        return SPIO
    if(SLIO[0] == 0):
        if(int(SPIO[0]) == SLIO[1]):
            return SPIO
    if(SPIO[0] == 0):
        if(int(SLIO[0]) == SPIO[1]):
            return SLIO

    return 0, 0

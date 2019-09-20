import json


def Special_Instructions_Processing(QTY, str):
    # https://stackoverflow.com/a/4289557
    if(str == False):
        return 0, 0

    Numbers = [int(s) for s in str.split() if s.isdigit()]

    if(len(Numbers) != 0):

        if(QTY == min(Numbers) * max(Numbers)):
            return min(Numbers), max(Numbers)
        if(QTY == min(Numbers) == max(Numbers)):
            return 1, max(Numbers)
        if(min(Numbers) == max(Numbers)):
           if(QTY % min(Numbers) == 0):
               if("every" in str or "each" in str or "into" in str):
                    return int(QTY / min(Numbers)), min(Numbers)
        return 0, 0
    else:
        return 1, QTY


def Special_Instructions(JOB_INFO):
    SPINumbers = JOB_INFO.get('Special Instructions', False)
    ShrinkNumbers = JOB_INFO.get('Slip Sheets / Shrink Wrap', False)
    QTY = int(JOB_INFO.get('Copies', False))
    SPIO = Special_Instructions_Processing(QTY, SPINumbers)
    SLIO = Special_Instructions_Processing(QTY, ShrinkNumbers)

    if (SPIO == SLIO):
        return SPIO
    if(SPIO == (0, 0)):
        return SLIO
    if(SLIO == (0, 0)):
        return SPIO

    return 0, 0

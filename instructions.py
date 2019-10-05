__version__ = "v20191005"

import json


def Special_Instructions_Processing(QTY, str):
    if(str == False):
        return 0, 0
    # Remove Unwanted Characters
    str = str.lower().replace('"', " ").replace('-', " ").replace('.',
                                                                  " ").replace('th ', " ").replace(', ', " ").replace('2 sided', " ").replace('1 sided', " ")
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
        if(QTY == max(Numbers)):
            Numbers.remove(max(Numbers))
            if(QTY == min(Numbers) * max(Numbers)):
                return min(Numbers), max(Numbers)
            return 0, 1
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


def default(JOB_INFO):
    if((JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and JOB_INFO.get('Stapling', False) != "Upper Left - landscape") and JOB_INFO.get('Drilling', False) != "Yes"):
        print('No Finishing')
        return str.encode(
            '@PJL XCPT <value syntax="enum">3</value>\n')
    else:
        return str.encode('')


def collation(JOB_INFO):
    if(JOB_INFO.get('Collation', False) == "Collated"):
        print('Collated')
        return str.encode(
            '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
    else:
        print('UnCollated')
        return str.encode(
            '@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')


def duplex(JOB_INFO):
    if(JOB_INFO.get('Duplex', False) == "Two-sided (back to back)"):
        print('Double Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>\n'), 2
    else:
        print('Single Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">one-sided</sides>\n'), 1


def stapling(JOB_INFO, collation):
    if(JOB_INFO.get('Stapling', False) == "Upper Left - portrait"):
        stapling = str.encode(
            '@PJL XCPT <value syntax="enum">20</value>\n')
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
            print("Collation Overide - Collated")
        print("Staple - Upper Left - portrait")
        return stapling, collation
    elif(JOB_INFO.get('Stapling', False) == "Upper Left - landscape"):
        stapling = str.encode(
            '@PJL XCPT <value syntax="enum">21</value>\n')
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
            print("Collation Overide - Collated")
        print("Staple - Upper Left - landscape")
        return stapling, collation
    else:
        return str.encode(''), collation


def drilling(JOB_INFO):
    if(JOB_INFO.get('Drilling', False) == "Yes"):
        print('Hole Punched')
        return str.encode(
            '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n')
    else:
        return str.encode('')


def weight_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    paper = (str(JOB_INFO.get('Paper', False))).lower()
    out = "stationery-heavyweight" if "card stock" in paper else "use-ready"
    print(out)
    return str.encode(
        '@PJL XCPT <media-type syntax="keyword">' + out + '</media-type>\n')


def color_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    color = (str(JOB_INFO.get('Paper', False))).split()[-1].lower()
    out = 'yellow' if color == 'canary' else color
    print(out)
    return str.encode(
        '@PJL XCPT <media-color syntax="keyword">' + out + '</media-color>\n')


def pjl_insert(JOB_INFO, COPIES_PER_SET, page_counts):
    print('\nChosen Options:')

    COLLATION = collation(JOB_INFO)
    DUPLEX, duplex_state = duplex(JOB_INFO)
    STAPLING, COLLATION = stapling(JOB_INFO, COLLATION)
    hole_punch = drilling(JOB_INFO)
    DEFAULT = default(JOB_INFO)
    media_color = color_extract(JOB_INFO)
    media_type = weight_extract(JOB_INFO)

    COPIES_COMMAND = str.encode(
        '@PJL XCPT <copies syntax="integer">'+str(COPIES_PER_SET)+'</copies>\n')
    with open('PJL_Commands/PJL.ps', 'rb') as f:
        lines = f.readlines()
    # Modifies the PJL file before adding it to the postscript files
    for i in range(len(lines)):
        if str('<media-color syntax="keyword">') in str(lines[i]):
            lines[i] = media_color
        if str('<media-type syntax="keyword">') in str(lines[i]):
            lines[i] = media_type
        if str('<copies syntax="integer">') in str(lines[i]):
            lines[i] = COPIES_COMMAND
        if str('<value syntax="enum">3</value>') in str(lines[i]):
            lines[i] = DEFAULT
            if str('<value syntax="enum">3</value>') not in str(DEFAULT):
                lines.insert(i, STAPLING)
                lines.insert(i+1, hole_punch)
        if str('<sheet-collate syntax="keyword">') in str(lines[i]):
            lines[i] = COLLATION
        if str('<sides syntax="keyword">one-sided</sides>') in str(lines[i]):
            lines[i] = DUPLEX
        if str('<sheet-collate syntax="keyword">uncollated') in str(COLLATION) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]):
            lines[i] = str.encode(
                '@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            lines.insert(i, str.encode(
                '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n'))
            print("\nSplit-Sheeting!")
        # Add SlipSheets to Large Collated Sets
        if (page_counts / len(JOB_INFO.get('Files', False)) / duplex_state >= 10 and str('<sheet-collate syntax="keyword">collated') in str(COLLATION) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]) and
                JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and (JOB_INFO.get('Stapling', False) != "Upper Left - landscape")):
            lines[i] = str.encode(
                '@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            lines.insert(i, str.encode(
                '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n'))
            print("\nSplit-Sheeting!")

    # The Postscript/PJL commands file that gets inserted before the file.
    with open('PJL_Commands/input.ps', 'wb') as f:
        for item in lines:
            f.write(item)
    # If it makes sense to use merged files, it uses them.
    if str('<sheet-collate syntax="keyword">uncollated') in str(COLLATION) and len(JOB_INFO.get('Files', False)) != 1:
        if page_counts / len(JOB_INFO.get('Files', False)) / duplex_state >= 10:
            print("DUE TO PAGE COUNT, MERGED TURNED OFF")
            return False
        else:
            print("THESE FILES WERE MERGED!")
            return True
    return False

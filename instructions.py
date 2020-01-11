__version__ = "v20201011"

import json
import PostScript


def duplex_state(JOB_INFO):
    if(JOB_INFO.get('Duplex', False) == "Two-sided (back to back)"):
        print('Double Sided')
        return 2
    else:
        print('Single Sided')
        return 1


def merging(JOB_INFO, PAGE_COUNTS):

    if JOB_INFO.get('Collation', False) == "Uncollated" and JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and len(JOB_INFO.get('Files', False)) != 1:
        if PAGE_COUNTS / len(JOB_INFO.get('Files', False)) / duplex_state(JOB_INFO) >= 10:
            print("DUE TO PAGE COUNT, MERGED TURNED OFF")
            return 0
        else:
            return 1
    elif len(JOB_INFO.get('Files', False)) != 1 and PAGE_COUNTS == len(JOB_INFO.get('Files', False)):
        return 1
    else:
        print("Not Merging")
        return 0


def Special_Instructions_Processing(QTY, str):
    if(str == False):
        return 0, 0
    # Remove Unwanted Characters
    str = str.lower().replace('"', " ").replace('-', " ").replace('.',
                                                                  " ").replace('th ', " ").replace(', ', " ").replace('2 sided', " ").replace('1 sided',
                                                                                                                                              " ").replace('!', " ")
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
            if("every" in str or "each" in str or "into" in str or "between" in str or "stacks of" in str or "sets of" in str):
                if(QTY % min(Numbers) == 0):
                    if(min(Numbers) <= 5):
                        return min(Numbers), int(QTY / min(Numbers))
                    else:
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
        if("set" in str or "slip" in str or "page" in str or "sort" in str or "group" in str or "into" in str):
            return 0, 1
        if((QTY * 2) == min(Numbers) * max(Numbers)):
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
    if((JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and JOB_INFO.get('Stapling', False) != "Upper Left - landscape" and JOB_INFO.get('Stapling', False) != "Double Left - portrait")
       and JOB_INFO.get('Drilling', False) != "Yes" and JOB_INFO.get('Booklets', False) != "Yes"):
        print('No Finishing')
        return str.encode(
            '@PJL XCPT <value syntax="enum">3</value>\n')
    else:
        return str.encode('')


def collation(JOB_INFO, page_counts):
    if(JOB_INFO.get('Collation', False) != "Collated" or (len(JOB_INFO.get('Files', {})) != 1 and page_counts == len(JOB_INFO.get('Files', {})))):
        print('UnCollated')
        return str.encode(
            '@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>\n')
    else:
        print('Collated')
        return str.encode(
            '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')


def duplex(JOB_INFO):
    if(JOB_INFO.get('Duplex', False) == "Two-sided (back to back)"):
        print('Double Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>\n'), 2
    elif(JOB_INFO.get('Duplex', False) == "two-sided-short-edge"):
        print('Double Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">two-sided-short-edge</sides>\n'), 2
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
    elif(JOB_INFO.get('Stapling', False) == "Double Left - portrait"):
        stapling = str.encode(
            '@PJL XCPT <value syntax="enum">28</value>\n')
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>\n')
            print("Collation Overide - Collated")
        print("Staple - Double Left - portrait")
        return stapling, collation
    else:
        return str.encode(''), collation


def drilling(JOB_INFO):
    if(JOB_INFO.get('Drilling', False) == "Yes"):
        print('Hole Punched')
        if("11 x 17" in str(JOB_INFO.get('Paper', False)).lower()):
            return str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">96</value>\n')
        else:
            return str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>\n')
    else:
        return str.encode('')


def weight_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    paper = (str(JOB_INFO.get('Paper', False))).lower()
    out = "stationery-heavyweight" if "card stock" in paper else "use-ready"
    print(out)
    return str.encode("".join([
        '@PJL XCPT <media-type syntax="keyword">', out, '</media-type>\n']))


def color_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    color = (str(JOB_INFO.get('Paper', False))).split()[-1].lower()
    out = 'yellow' if color == 'canary' else color
    print(out)
    return str.encode("".join(['@PJL XCPT <media-color syntax="keyword">', out, '</media-color>\n']))


def size_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    paper = (str(JOB_INFO.get('Paper', False))).lower()
    if "8.5 x 11" in paper:
        print("letter")
        return str.encode("")
    if "11 x 17" in paper:
        print("ledger")
        return str.encode("".join(['\
@PJL XCPT 				<media-size syntax="collection">\n\
@PJL XCPT 					<x-dimension syntax="integer">27940</x-dimension>\n\
@PJL XCPT 					<y-dimension syntax="integer">43180</y-dimension>\n\
@PJL XCPT 				</media-size>\n']))


def cover_weight_extract(PAPER):
    # Converts Input from given form to the value the printer needs
    paper = (str(PAPER)).lower()
    out = "stationery-heavyweight" if "card stock" in paper else "use-ready"
    print(out)
    return out


def cover_color_extract(PAPER):
    # Converts Input from given form to the value the printer needs
    color = (str(PAPER)).split()[-1].lower()
    out = 'yellow' if color == 'canary' else color
    print(out)
    return out


def booklet_extract(JOB_INFO):
    # Converts Input from given form to the value the printer needs
    if JOB_INFO.get('Booklets', False) == "Yes":
        return str.encode("".join(['@PJL XCPT <value syntax="enum">110</value>\n']))
    return ""


def covers(JOB_INFO, COVERS):
    if(COVERS):
        Back = ""
        if(JOB_INFO.get('Back Cover', False)):
            print("Back Cover")
            Back_Cover_Color = cover_color_extract(
                JOB_INFO.get('Back Cover', False))
            Back_Cover_Weight = cover_weight_extract(
                JOB_INFO.get('Back Cover', False))
            Back = "".join(['\
@PJL XCPT 		<cover-back syntax="collection">\n\
@PJL XCPT 			<cover-type syntax="keyword">print-none</cover-type>\n\
@PJL XCPT 			<media-col syntax="collection">\n\
@PJL XCPT 				<media-color syntax="keyword">', Back_Cover_Color, '</media-color>\n\
@PJL XCPT 				<media-type syntax="keyword">', Back_Cover_Weight, '</media-type>\n\
@PJL XCPT 			</media-col>\n\
@PJL XCPT 		</cover-back>\n'])
        Front = ""
        if(JOB_INFO.get('Front Cover', False)):
            print("Front Cover")
            Front_Cover_Color = cover_color_extract(
                JOB_INFO.get('Front Cover', False))
            Front_Cover_Weight = cover_weight_extract(
                JOB_INFO.get('Front Cover', False))
            Front = "".join(['\
@PJL XCPT <page-overrides syntax="1setOf">\n\
@PJL XCPT 			<value syntax="collection">\n\
@PJL XCPT 				<input-documents syntax="1setOf">\n\
@PJL XCPT 					<value syntax="rangeOfInteger">\n\
@PJL XCPT 						<lower-bound syntax="integer">1</lower-bound>\n\
@PJL XCPT 						<upper-bound syntax="integer">1</upper-bound>\n\
@PJL XCPT 					</value>\n\
@PJL XCPT 				</input-documents>\n\
@PJL XCPT 				<media-col syntax="collection">\n\
@PJL XCPT 					<media-color syntax="keyword">', Front_Cover_Color, '</media-color>\n\
@PJL XCPT 					<media-type syntax="keyword">', Front_Cover_Weight, '</media-type>\n\
@PJL XCPT 				</media-col>\n\
@PJL XCPT 				<pages syntax="1setOf">\n\
@PJL XCPT 					<value syntax="rangeOfInteger">\n\
@PJL XCPT 						<lower-bound syntax="integer">1</lower-bound>\n\
@PJL XCPT 						<upper-bound syntax="integer">1</upper-bound>\n\
@PJL XCPT 					</value>\n\
@PJL XCPT 				</pages>\n\
@PJL XCPT 				<sides syntax="keyword">one-sided</sides>\n\
@PJL XCPT 			</value>\n\
@PJL XCPT 		</page-overrides>\n'])
        return ("".join([Back, Front]))
    return ""


def pjl_insert(JOB_INFO, COPIES_PER_SET, page_counts, COVERS):
    print('\nChosen Options:')

    COLLATION = collation(JOB_INFO, page_counts)
    DUPLEX, duplex_state = duplex(JOB_INFO)
    STAPLING, COLLATION = stapling(JOB_INFO, COLLATION)
    hole_punch = drilling(JOB_INFO)
    DEFAULT = default(JOB_INFO)
    media_color = color_extract(JOB_INFO)
    media_type = weight_extract(JOB_INFO)
    booklet = booklet_extract(JOB_INFO)
    COVER = covers(JOB_INFO, COVERS)
    size = size_extract(JOB_INFO)
    COPIES_COMMAND = str.encode("".join(
        ['@PJL XCPT <copies syntax="integer">', str(COPIES_PER_SET), '</copies>\n', COVER]))
    with open('PJL_Commands/PJL.ps', 'rb') as f:
        lines = f.readlines()
    # Modifies the PJL file before adding it to the postscript files
    for i in range(len(lines)):
        if str('<media-color syntax="keyword">') in str(lines[i]):
            lines[i] = media_color
            lines.insert(i+1, size)
        if str('<media-type syntax="keyword">') in str(lines[i]):
            lines[i] = media_type
        if str('<copies syntax="integer">') in str(lines[i]):
            lines[i] = COPIES_COMMAND
            continue
        if str('<value syntax="enum">3</value>') in str(lines[i]):
            lines[i] = DEFAULT
            if str('<value syntax="enum">3</value>') not in str(DEFAULT) and booklet == "":
                lines.insert(i, STAPLING)
                lines.insert(i+1, hole_punch)
            elif(booklet != ""):
                lines.insert(i, booklet)
        if str('<sheet-collate syntax="keyword">') in str(lines[i]):
            lines[i] = COLLATION
        if str('<sides syntax="keyword">one-sided</sides>') in str(lines[i]):
            lines[i] = DUPLEX
        if str('<sheet-collate syntax="keyword">uncollated') in str(COLLATION) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]):

            if("11 x 17" in str(JOB_INFO.get('Paper', False)).lower()):
                lines[i] = str.encode(
                    '@PJL XCPT <media-col syntax="collection">\n@PJL XCPT <input-tray syntax="keyword">bypass-tray</input-tray>\n@PJL XCPT <tray-feed syntax="keyword">stack</tray-feed>\n@PJL XCPT </media-col>\n@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            else:
                lines[i] = str.encode(
                    '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n@PJL XCPT 	<separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            print("\nSplit-Sheeting!")
        # Add SlipSheets to Large Collated Sets
        if (page_counts / len(JOB_INFO.get('Files', False)) / duplex_state >= 10 and str('<sheet-collate syntax="keyword">collated') in str(COLLATION) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]) and
                JOB_INFO.get('Stapling', False) != "Upper Left - portrait" and (JOB_INFO.get('Stapling', False) != "Upper Left - landscape") and JOB_INFO.get('Stapling', False) != "Double Left - portrait"):

            if("11 x 17" in str(JOB_INFO.get('Paper', False)).lower()):
                lines[i] = str.encode(
                    '@PJL XCPT<media-col syntax="collection">\n@PJL XCPT <input-tray syntax="keyword">bypass-tray</input-tray>\n@PJL XCPT <tray-feed syntax="keyword">stack</tray-feed>\n@PJL XCPT </media-col>\n@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            else:
                lines[i] = str.encode(
                    '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n@PJL XCPT 	<separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>\n')
            print("\nSplit-Sheeting!")
        if str('<output-bin syntax="keyword">') in str(lines[i]) and booklet != "":
            lines[i] = str.encode(
                '@PJL XCPT 		<output-bin syntax="keyword">automatic</output-bin>\n')

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
    elif len(JOB_INFO.get('Files', False)) != 1 and page_counts == len(JOB_INFO.get('Files', False)):
        return True
    return False


def cover_manual(OUTPUT_DIRECTORY, ORDER_NAME, JOB_INFO):
    while True:
        try:
            file_order = input(
                "Select Order of Files (Separate File Numbers by Space. EX: 1 2): ")
            file_order = [int(s) for s in file_order.split() if s.isdigit()]
            break
        except:
            pass
    FILES = []
    while True:
        try:
            DUPLEX_STATE = int(
                input("Duplex Merge? 2 Yes - 1 No (Default: 2): "))
            break
        except:
            pass
    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    for files in file_order:
        JOB_INFO_FILES = JOB_INFO.get('Files', False)
        FILE_INFO = JOB_INFO_FILES.get(" ".join(["File", str(files)]), False)
        FILES.append(FILE_INFO.get("File Name", False))
    return PostScript.file_merge_manual(OUTPUT_DIRECTORY, ORDER_NAME, DUPLEX_STATE, FILES)

__version__ = "v20200925"
import PostScript
from PJL_Commands.PJL_PS import end
from PJL_Commands.PJL_PS import start
import log
import re
import os


def duplex_state(order):
    """
    Checks if the Order is set to Duplex or not.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        int: Duplex State
    """
    if(order.DUPLEX == "Two-sided (back to back)"):
        print('Double Sided')
        return 2
    else:
        print('Single Sided')
        return 1


def merging(order):
    """
    Determines if the job should be merged or not.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        bool: Merge status
    """
    if order.COLLATION == "Uncollated" and order.STAPLING != "Upper Left - portrait" and len(order.FILES) != 1:
        if order.PAGE_COUNTS / len(order.FILES) / duplex_state(order) >= 5:
            print("DUE TO PAGE COUNT, MERGED TURNED OFF")
            return 0
        else:
            return 1
    elif len(order.FILES) != 1 and order.PAGE_COUNTS == len(order.FILES):
        order.DUPLEX = "One-sided"
        order.STAPLING = ""
        return 1
    else:
        print("Not Merging")
        return 0


def Special_Instructions_Processing(QTY, str):
    """
    Determines the amount of sets, and copies per set for a given string and quantity.

    Parameters: 
        QTY (int): The total copy quantity of the job.
        str (str): The string that needs to be analyzed.

    Returns: 
        int: The amount of sets.
        int: The amount of copies per set.
    """
    if(str == False):
        return 0, 0
    # Remove Unwanted Characters
    str = re.sub(r'[.\-!\",]', " ", str.lower())
    str = str.replace('th ', " ").replace(
        '1 to 2 sided', " ").replace(
        '2 sided', " ").replace('1 sided', " ")
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
            if(any(s in str for s in ("every", "each", "into", "between", "stacks of", "sets of"))):
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
        if(any(s in str for s in ("set", "slip", "page", "sort", "group", "into"))):
            return 0, 1
        if((QTY * 2) == min(Numbers) * max(Numbers)):
            return 0, 1
        return 0, 0
    else:
        return 0, 0


def Special_Instructions(order):
    """
    Determines the amount of sets, and copies per set for an order.

    Using the Special Instructions Field,
    and the Shrink Wrap / Slip Sheets Field,
    and the Total Copies Field,
    The amount of sets, and copies per set are calculated.

    If the output cannot be determined, it defaults to human input later.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        int: The amount of sets.
        int: The amount of copies per set.
        (Or 0,0 for inconclusive)
    """
   # Get Information from JSON file, QTY, Comment Line #1 & #2
   # Process the information from both comment sections
    QTY = order.COPIES
    SPIO = Special_Instructions_Processing(QTY, order.SPECIAL_INSTRUCTIONS)
    SLIO = Special_Instructions_Processing(QTY, order.SLIPSHEETS)
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


def default(order):
    """
    Sets the flag for no Finishing for the printer.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    if(order.STAPLING_BOOL == False and order.DRILLING != "Yes" and order.BOOKLET != "Yes"):
        print('No Finishing')
        return str.encode(
            '@PJL XCPT <value syntax="enum">3</value>')
    else:
        return str.encode('')


def collation(order):
    """
    Determines whether the order is collated or uncollated.

    Based on the the resquest of the customer, and how many and how long the documents are,
    the job will either be run collated, or uncollated.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    if(order.COLLATION != "Collated" or (len(order.FILES)) != 1 and order.PAGE_COUNTS == len(order.FILES)):
        print('UnCollated')
        return str.encode(
            '@PJL XCPT <sheet-collate syntax="keyword">uncollated</sheet-collate>')
    else:
        print('Collated')
        return str.encode(
            '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>')


def duplex(order):
    """
    Determines whether the order is duplex or not.

    Depending on the order, it can be either
    Single Sided
    Double Sided Long Edge
    Double SIded Short Edge

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    if(order.DUPLEX == "Two-sided (back to back)"):
        print('Double Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">two-sided-long-edge</sides>'), 2
    elif(order.DUPLEX == "two-sided-short-edge"):
        print('Double Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">two-sided-short-edge</sides>'), 2
    else:
        print('Single Sided')
        return str.encode(
            '@PJL XCPT <sides syntax="keyword">one-sided</sides>'), 1


def stapling(order, collation):
    """
    Determines if and what stapling is required.

    Depending on the order, it can be either
    Top Left Portait
    Top Left Landscape
    Double Left Staple
    Based on the order, collation and/or stapling 
    can be overridden if input is unreasonable.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code for Stapling
        str: PJL Code for Collation
    """
    if(order.STAPLING == "Upper Left - portrait"):
        stapling = str.encode(
            '@PJL XCPT <value syntax="enum">20</value>')
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>')
            print("Collation Overide - Collated")
        print("Staple - Upper Left - portrait")
        return stapling, collation
    elif(order.STAPLING == "Upper Left - landscape"):
        stapling = str.encode(
            '@PJL XCPT <value syntax="enum">21</value>')
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>')
            print("Collation Overide - Collated")
        print("Staple - Upper Left - landscape")
        return stapling, collation
    elif(order.STAPLING == "Double Left - portrait"):
        stapling = str.encode(
            '@PJL XCPT <value syntax="enum">28</value>')
        if str('<sheet-collate syntax="keyword">uncollated') in str(collation):
            collation = str.encode(
                '@PJL XCPT <sheet-collate syntax="keyword">collated</sheet-collate>')
            print("Collation Overide - Collated")
        print("Staple - Double Left - portrait")
        return stapling, collation
    else:
        return str.encode(''), collation


def drilling(order):
    """
    Checks if the order should be Three-Hole Punched.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    if(order.DRILLING == "Yes"):
        print('Hole Punched')
        if("11 x 17" in str(order.PAPER).lower()):
            return str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">94</value>')
        else:
            return str.encode(
                '@PJL XCPT  <value syntax="enum">91</value> \n@PJL XCPT <value syntax="enum">93</value>')
    else:
        return str.encode('')


def weight_extract(order):
    """
    Determines if the order is on paper or cardstock.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    paper = (str(order.PAPER)).lower()
    out = "stationery-heavyweight" if "card stock" in paper else "use-ready"
    print(out)
    return str.encode("".join([
        '@PJL XCPT <media-type syntax="keyword">', out, '</media-type>']))


def color_extract(order):
    """
    Determines the color of the paper.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    color = (str(order.PAPER)).split()[-1].lower()
    out = 'yellow' if color == 'canary' else color
    print(out)
    return str.encode("".join(['@PJL XCPT <media-color syntax="keyword">', out, '</media-color>']))


def size_extract(order):
    """
    Determines the size of the paper.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    # Checks the size of the paper
    paper = (str(order.PAPER)).lower()
    if "8.5 x 11" in paper:
        print("letter")
        return str.encode("")
    if "11 x 17" in paper:
        print("ledger")
        return str.encode("".join(['\
@PJL XCPT 				<media-size syntax="collection">\n\
@PJL XCPT 					<x-dimension syntax="integer">27940</x-dimension>\n\
@PJL XCPT 					<y-dimension syntax="integer">43180</y-dimension>\n\
@PJL XCPT 				</media-size>']))


def booklet_extract(order):
    """
    Determines wether the order needs to be saddle-stitched or not.

    Parameters: 
        order   (object): The object containing all the information for the current order.

    Returns: 
        str: PJL Code
    """
    # Determines if the order is a booklet
    if order.BOOKLET == "Yes":
        return str.encode("".join(['@PJL XCPT <value syntax="enum">110</value>']))
    return ""


def pjl_merge(order, outFOLDER, MERGED, FILES):
    """
    Merges the Postscript files with the custom PJL header file to create Print Ready Postscript Files.

    Parameters: 
        order       (object): The object containing all the information for the current order.
        outFOLDER   (str)   : The output folder to store the Print Ready files inside.
        MERGED      (bool)  : Determines if thier is a single merged document or individual Files.
        FILES       (list)  : The list of files that will be merged.

    Returns: 
        bool: unused return.
    """
    # TODO: merged default param
    N = "n" if outFOLDER == "PSPn" else ""
    F = order.OD + "/"+order.NAME + "/" + outFOLDER
    try:
        if not os.path.exists(F):
            os.makedirs(F)
            print("Successfully created the directory ", F)
    except OSError:
        print("Creation of the directory failed ", F)
    if MERGED == True:
        # Add the PJL Commands to the merged file in preperation to print.
        file_names = ['input.ps', order.OD+"/" +
                      order.NAME + "/"+order.NAME+N+".ps"]
        with open(order.OD+"/"+order.NAME + "/"+outFOLDER + "/"+order.NAME+".ps", 'wb') as outfile:
            for fname in file_names:
                with open(fname, 'rb') as infile:
                    for line in infile:
                        outfile.write(line)
            for line in end.splitlines():
                outfile.write(line)
        return 1
    elif MERGED == False:
        # Add the PJL Commands to the files in preperation to print.
        for i in range(len(FILES)):
            file_names = ['input.ps', order.OD+"/"+order.NAME +
                          "/PostScript"+N+"/"+FILES[i]+".ps"]
            with open(order.OD+"/"+order.NAME + "/" + outFOLDER + "/"+FILES[i][:40][:-4]+".ps", 'wb') as outfile:
                for fname in file_names:
                    with open(fname, 'rb') as infile:
                        for line in infile:
                            outfile.write(line)
                for line in end.splitlines():
                    outfile.write(line)
        return 1
    return 0


def pjl_insert(order, COPIES_PER_SET):
    """
    Generates the Custom PJL Header File and
    Inserts the Printer Commands into the final print ready file(s).

    Parameters: 
        order           (object): The object containing all the information for the current order.
        COPIES_PER_SET  (str)   : The amount of copies per set.

    Returns: 
        bool: unused return.
    """
    print('\nChosen Options:')
    COLLATION = collation(order)
    DUPLEX, duplex_state = duplex(order)
    STAPLING, COLLATION = stapling(order, COLLATION)
    hole_punch = drilling(order)
    DEFAULT = default(order)
    media_color = color_extract(order)
    media_type = weight_extract(order)
    booklet = booklet_extract(order)
    size = size_extract(order)
    COPIES_COMMAND = str.encode("".join(
        ['@PJL XCPT <copies syntax="integer">', str(COPIES_PER_SET), '</copies>']))
    lines = start.splitlines()
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
            if("11 x 17" in str(order.PAPER).lower()):
                lines[i] = str.encode(
                    '@PJL XCPT <media-col syntax="collection">\n@PJL XCPT <input-tray syntax="keyword">bypass-tray</input-tray>\n@PJL XCPT <tray-feed syntax="keyword">stack</tray-feed>\n@PJL XCPT </media-col>\n@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>')
            else:
                lines[i] = str.encode(
                    '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n@PJL XCPT 	<separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>')
            print("\nSplit-Sheeting!")
        # Add SlipSheets to Large Collated Sets
        if (order.PAGE_COUNTS / len(order.FILES) / duplex_state >= 10 and str('<sheet-collate syntax="keyword">collated') in str(COLLATION) and str('<separator-sheets-type syntax="keyword">none') in str(lines[i]) and
                order.STAPLING_BOOL == False):
            if("11 x 17" in str(order.PAPER).lower()):
                lines[i] = str.encode(
                    '@PJL XCPT<media-col syntax="collection">\n@PJL XCPT <input-tray syntax="keyword">bypass-tray</input-tray>\n@PJL XCPT <tray-feed syntax="keyword">stack</tray-feed>\n@PJL XCPT </media-col>\n@PJL XCPT <separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>')
            else:
                lines[i] = str.encode(
                    '@PJL XCPT <media syntax="keyword">post-fuser-inserter</media>\n@PJL XCPT 	<separator-sheets-type syntax="keyword">end-sheet</separator-sheets-type>')
            print("\nSplit-Sheeting!")
        if str('<output-bin syntax="keyword">') in str(lines[i]) and booklet != "":
            lines[i] = str.encode(
                '@PJL XCPT 		<output-bin syntax="keyword">automatic</output-bin>')
    # The Postscript/PJL commands file that gets inserted before the file.
    with open('input.ps', 'wb') as f:
        for item in lines:
            f.write(item)
            if len(item):
                f.write(b"\n")
    # If it makes sense to use merged files, it uses them.
    if str('<sheet-collate syntax="keyword">uncollated') in str(COLLATION) and len(order.FILES) != 1:
        if order.PAGE_COUNTS / len(order.FILES) / duplex_state >= 5:
            print("DUE TO PAGE COUNT, MERGED TURNED OFF")
            return False
        else:
            print("THESE FILES WERE MERGED!")
            return True
    elif len(order.FILES) != 1 and order.PAGE_COUNTS == len(order.FILES):
        return True
    return False

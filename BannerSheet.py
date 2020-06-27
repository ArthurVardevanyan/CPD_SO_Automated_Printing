# BannerSheet.py
__version__ = "v20200627"
# Setups up BannerSheet Postscript File
from PJL_Commands.BannerSheetPS import bannerSheet


def banner_sheet(order):
    OUTPUT_PATH = "".join([order.OD, '/', order.NAME, '/'])
    NAME = "", "Print & Copy"
    LOC = ""
    try:
        with open("Credentials/creds.txt") as f:
            cred = f.readlines()
        cred = [x.strip() for x in cred]
        NAME = (str(cred[1]), str(cred[2]))
        LOC = str(cred[3])
    except:
        print("Credential Failure")
    MEDIA_COLOR = ("white", "blue", "yellow", "green", "pink",
                   "ivory", "gray", "buff", "goldenrod,", "red", "orange")
    # Allows differnet color banner sheets. Common Pastel/Astrobrights Colors
    banner_sheet_color = MEDIA_COLOR[6]
    # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
    pjl_lines = bannerSheet.splitlines()
    # Swap template color for color of choice
    for i in range(len(pjl_lines)):
        if str('<media-color syntax="keyword">') in str(pjl_lines[i]):
            pjl_lines[i] = str.encode("".join([
                '@PJL XCPT <media-color syntax="keyword">', banner_sheet_color, '</media-color>']))
    # Get the nested dictionary for file names & page counts from main dictionary from JSON File
    files_list = []
    for i in range(len(order.FILES)):
        files_list.append(("".join(["File ",
                                    str(i+1), ": ", order.FILES[i].NAME[13:]]), "".join(["Page Count: ", str(order.FILES[i].PAGE_COUNT)])))  # Remove clutter from string
    # Template Postscript information
    POSTSCRIPT = (
        "".join(['\n%!PS\n', '/Arial-BoldMT findfont 75 scalefont setfont\n', '95 725 moveto (',
                 NAME[0], ') show\n']),
        "".join(['\n%!PS\n', '/Arial-BoldMT findfont 74 scalefont setfont\n', '85 650 moveto (',
                 NAME[1], ') show\n']),
        "".join(['/Arial-BoldMT findfont 45 scalefont setfont\n']),
        "".join(['20 595 moveto (Order Number: ',
                 order.NUMBER, ' ) show\n']),
        "".join(['/Arial-BoldMT findfont 25 scalefont setfont\n']),
        "".join(['20 565 moveto (', LOC, ' - School Order Banner Sheet) show\n']),
        "".join(['/ArialMT findfont 12 scalefont setfont\n']),
    )
    vertical_position = int(545)
    # Create Banner Sheet file with Order Number and Teacher Name
    with open("".join([OUTPUT_PATH,  order.NUMBER, ' Banner ',  order.FIRST_NAME, ' ', order.LAST_NAME, '.ps']), 'wb') as outfile:
        # Export PJL Lines
        for lines in pjl_lines:
            outfile.write(lines + b"\n")
        # Export Postscript Lines
        for line in POSTSCRIPT:
            outfile.write(str.encode(line))
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Order Subject: ", order.SUBJECT, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Date Ordered: ", order.DATE, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Email: ", order.EMAIL, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Last Name: ", order.LAST_NAME, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "First Name: ", order.FIRST_NAME, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Phone Number: ", order.PHONE, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Copies: ", str(order.COPIES), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Duplex: ", order.DUPLEX, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Collation: ", order.COLLATION, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Paper: ", order.PAPER, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Special Instructions: ", str(order.SPECIAL_INSTRUCTIONS), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Slip Sheets / Shrink Wrap: ", str(order.SLIPSHEETS), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Deliver To Name: ", order.DELIVER_TO_NAME, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['20 ', str(
            vertical_position), ' moveto (', "Deliver To Address: ", str(order.DELIVER_TO_ADDRESS), ' ) show\n'])))
        vertical_position = int(vertical_position) - 25
        # Export Files & Page Counts
        for items in files_list:
            outfile.write(str.encode("".join(['20 ', str(vertical_position),
                                              ' moveto (', str(items[0]).replace("(", " ").replace(")", " ").split("', '")[0], ' ) show\n'])))
            vertical_position = int(vertical_position) - 15
            outfile.write(str.encode("".join(['20 ', str(vertical_position),
                                              ' moveto (', str(items[1]).replace("(", " ").replace(")", " ").split("', '")[0], ' ) show\n'])))
            vertical_position = int(vertical_position) - 17
        # Write Final Line of Postscript File
        outfile.write(str.encode('showpage\n'))
    # Return Location of Banner Sheet File
    return "".join([OUTPUT_PATH, order.NUMBER, ' Banner ', order.FIRST_NAME, ' ', order.LAST_NAME, '.ps'])

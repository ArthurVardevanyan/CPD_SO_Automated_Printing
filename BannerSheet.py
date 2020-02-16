# BannerSheet.py
__version__ = "v20200131"


# Setups up BannerSheet Postscript File
def banner_sheet(order):

    OUTPUT_PATH = "".join([order.OD, '/', order.NAME, '/'])
    NAME = "CHANGE ME"
    LOC = "CHANGE ME"
    try:
        with open("Credentials/creds.txt") as f:
            cred = f.readlines()
        cred = [x.strip() for x in cred]
        NAME = str(cred[1])
        LOC = str(cred[2])
    except:
        print("Credential Failure")

    MEDIA_COLOR = ("white", "blue", "yellow", "green", "pink",
                   "ivory", "gray", "buff", "goldenrod,", "red", "orange")
    # Allows differnet color banner sheets. Common Pastel/Astrobrights Colors
    banner_sheet_color = MEDIA_COLOR[6]
    # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
    with open('PJL_Commands/BannerSheet.ps', 'rb') as f:
        pjl_lines = f.readlines()

    # Swap template color for color of choice
    for i in range(len(pjl_lines)):
        if str('<media-color syntax="keyword">') in str(pjl_lines[i]):
            pjl_lines[i] = str.encode("".join([
                '@PJL XCPT <media-color syntax="keyword">', banner_sheet_color, '</media-color>\n']))

    # Get the nested dictionary for file names & page counts from main dictionary from JSON File
    files_list = []
    for i in range(len(order.FILES)):
        files_list.append(("".join(["File ",
                                    str(i+1), ": ", order.FILES[i].NAME[13:]]), "".join(["Page Count: ", str(order.FILES[i].PAGE_COUNT)])))  # Remove clutter from string

    # Template Postscript information
    POSTSCRIPT = (
        "".join(['\n%!PS\n', '/Times-Bold findfont 70 scalefont setfont\n', '28 684 moveto (',
                 NAME, ') show\n']),
        "".join(['/Times-Bold findfont 25 scalefont setfont\n']),
        "".join(['75 650 moveto (', LOC, ' - School Order Banner Sheet) show\n']),
        "".join(['75 620 moveto (Order Number: ',
                 order.NUMBER, ' ) show\n']),
        "".join(['/Times findfont 12 scalefont setfont\n']),
    )
    vertical_position = int(600)
    # Create Banner Sheet file with Order Number and Teacher Name
    with open("".join([OUTPUT_PATH,  order.NUMBER, ' Banner ',  order.FIRST_NAME, ' ', order.LAST_NAME, '.ps']), 'wb') as outfile:
        # Export PJL Lines
        for lines in pjl_lines:
            outfile.write(lines)
        # Export Postscript Lines
        for line in POSTSCRIPT:
            outfile.write(str.encode(line))

        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Order Subject: ", order.SUBJECT, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Date Ordered: ", order.DATE, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Email: ", order.EMAIL, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Last Name: ", order.LAST_NAME, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "First Name: ", order.FIRST_NAME, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Phone Number: ", order.PHONE, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Copies: ", str(order.COPIES), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Duplex: ", order.DUPLEX, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Collation: ", order.COLLATION, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Paper: ", order.PAPER, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Special Instructions: ", str(order.SPECIAL_INSTRUCTIONS), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Slip Sheets / Shrink Wrap: ", str(order.SLIPSHEETS), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Deliver To Name: ", order.DELIVER_TO_NAME, ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        outfile.write(str.encode("".join(['75 ', str(
            vertical_position), ' moveto (', "Deliver To Address: ", str(order.DELIVER_TO_ADDRESS), ' ) show\n'])))
        vertical_position = int(vertical_position) - 17
        vertical_position = int(vertical_position) - 20
        # Export Files & Page Counts
        for items in files_list:
            outfile.write(str.encode("".join(['25 ', str(vertical_position),
                                              ' moveto (', str(items[0]).replace("(", " ").replace(")", " ").split("', '")[0], ' ) show\n'])))
            vertical_position = int(vertical_position) - 17
            outfile.write(str.encode("".join(['25 ', str(vertical_position),
                                              ' moveto (', str(items[1]).replace("(", " ").replace(")", " ").split("', '")[0], ' ) show\n'])))

            vertical_position = int(vertical_position) - 17
        # Write Final Line of Postscript File
        outfile.write(str.encode('showpage\n'))
    # Return Location of Banner Sheet File
    return "".join([OUTPUT_PATH, order.NUMBER, ' Banner ', order.FIRST_NAME, ' ', order.LAST_NAME, '.ps'])

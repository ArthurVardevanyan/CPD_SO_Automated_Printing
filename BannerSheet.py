import json

# Setups up BannerSheet Postscript File


def banner_sheet(JOB_INFO, OUTPUT_PATH):
    MEDIA_COLOR = ("white", "blue", "yellow", "green", "pink",
                   "ivory", "gray", "buff", "goldenrod,", "red", "orange")
    # Allows differnet color banner sheets. Common Pastel/Astrobrights Colors
    banner_sheet_color = MEDIA_COLOR[3]
    # Read in Template BannerSheet PostScript File with PJL Commands for Xerox D110 Printer
    with open('PJL_Commands/BannerSheet.ps', 'rb') as f:
        pjl_lines = f.readlines()

    # Swap template color for color of choice
    for i in range(len(pjl_lines)):
        if str('<media-color syntax="keyword">') in str(pjl_lines[i]):
            pjl_lines[i] = str.encode(
                '@PJL XCPT <media-color syntax="keyword">' + banner_sheet_color + '</media-color>\n')

    # Get the nested dictionary for file names & page counts from main dictionary from JSON File
    JOB_INFO_FILES = JOB_INFO.get('Files', False)
    files_list = []
    for items in JOB_INFO_FILES:
        files_list.append(
            items + ": " + str(JOB_INFO_FILES.get(items))[20:][:-1])  # Remove clutter from string

    # Template Postscript information
    POSTSCRIPT = (
        '\n%!PS\n', '/Times-Bold findfont 70 scalefont setfont\n', '28 684 moveto (Workonomy-CPD) show\n',
        '/Times-Bold findfont 25 scalefont setfont\n',
        '75 650 moveto (Store 06342 - School Order Banner Sheet) show\n',
        '75 620 moveto (Order Number: ' +
        JOB_INFO.get('Order Number', False) + ' ) show\n',
        '/Times findfont 12 scalefont setfont\n',
    )
    vertical_position = int(600)
    # Create Banner Sheet file with Order Number and Teacher Name
    with open(OUTPUT_PATH+JOB_INFO.get('Order Number', False) + ' Banner ' + JOB_INFO.get('First Name', False) + ' ' + JOB_INFO.get('Last Name', False) + '.ps', 'wb') as outfile:
        # Export PJL Lines
        for lines in pjl_lines:
            outfile.write(lines)
        # Export Postscript Lines
        for line in POSTSCRIPT:
            outfile.write(str.encode(line))
        # Export Job Info Dictionary
        for key, value in JOB_INFO.items():
            if(key != 'Files' and key != 'Ran'and key != 'Account ID'and key != 'Order Number' and key != 'Building'):
                outfile.write(str.encode('75 ' + str(vertical_position) +
                                         ' moveto ('+str(key) + ": " + str(value)+' ) show\n'))
                vertical_position = int(vertical_position) - 17
        vertical_position = int(vertical_position) - 20
        # Export Files & Page Counts
        for items in files_list:
            items = items.split("', '")
            outfile.write(str.encode('25 ' + str(vertical_position) +
                                     ' moveto ('+str(items[0]) + ' ) show\n'))
            vertical_position = int(vertical_position) - 17
            outfile.write(str.encode('25 ' + str(vertical_position) +
                                     ' moveto ('+str(items[1]) + ' ) show\n'))
            vertical_position = int(vertical_position) - 17
        # Write Final Line of Postscript File
        outfile.write(str.encode('showpage\n'))
    # Return Locatoin of Banner Sheet File
    return OUTPUT_PATH+JOB_INFO.get('Order Number', False) + ' Banner Sheet.ps'

import json


def bannerSheet(JobInfo, path):
    with open('PJL_Commands/BannerSheetRed', 'rb') as f:
        bannerlines = f.readlines()

    filedict = JobInfo.get('Files', False)
    filelist = []
    for items in filedict:
        filelist.append(items + ": " + str(filedict.get(items))[20:][:-1])

    PSFILE = [
        '\n%!PS\n', '/Times-Bold findfont 70 scalefont setfont\n', '28 684 moveto (Workonomy-CPD) show\n',
        '/Times-Bold findfont 25 scalefont setfont\n',
        '75 650 moveto (Store 06342 - School Order Banner Sheet) show\n',
        '75 620 moveto (Order Number: ' +
        JobInfo.get('Order Number', False) + ' ) show\n',
        '/Times findfont 12 scalefont setfont\n',
    ]
    vline = int(600)
    with open(path+JobInfo.get('Order Number', False) + ' Banner Sheet.ps', 'wb') as outfile:
        for lines in bannerlines:
            outfile.write(lines)

        for line in PSFILE:
            outfile.write(str.encode(line))
        for key, value in JobInfo.items():
            if(key != 'Files' and key != 'Ran'):
                outfile.write(str.encode('75 ' + str(vline) +
                                         ' moveto ('+str(key) + ": " + str(value)+' ) show\n'))
                vline = int(vline) - 17
        vline = int(vline) - 20
        for items in filelist:
            outfile.write(str.encode('25 ' + str(vline) +
                                     ' moveto ('+str(items) + ' ) show\n'))
            vline = int(vline) - 17
        outfile.write(str.encode('showpage\n'))
    return path+JobInfo.get('Order Number', False) + ' Banner Sheet.ps'

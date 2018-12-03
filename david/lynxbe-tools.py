import os
from Naked.toolshed.shell import execute_js, muterun_js

result = execute_js('data-collector.js')

if result: 
    os.system("statistics-generator.py")


from ftplib import FTP

def directory_exists(dirName):
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    return any(f.split()[-1] == dirName and f.upper().startswith('D') for f in filelist)

ftp = FTP('ftp.s485.upress.link')
ftp.login('ftp@lynxbe.co.il', 'CmtMyA-R@nRs-N')
ftp.cwd('statistics')

path = './'
userDirectories = [f for f in os.listdir(path) if os.path.isdir(path + '/' + f)]

for dir in userDirectories:
    if directory_exists(dir) == False:
        ftp.mkd(dir)
    ftp.cwd(dir)

    path = './' + dir
    userFiles = os.listdir(path)
    for fileName in userFiles:
        file = open(path + '/' + fileName,'rb')                  
        ftp.storbinary('STOR ' + fileName, file) 
        file.close()                                    

    ftp.cwd('..')
    print('Finished transfering ' + dir + ' files.')

ftp.quit()
'''
Input: MS Word generated html file.  
What it does: change encoding to utf-8, remove style info specific to Microsoft Outlook, replace curly double quotes (“) with straights (").  
'''

from tempfile import TemporaryFile
from os import path
import shutil
from myfile import sysArgvOrInput

MSO_9_START = '<!--[if gte mso '
MSO_9_END = '<![endif]-->'

def main():
    filename = sysArgvOrInput()
    with TemporaryFile() as tmp:
        with open(filename, 'r', encoding='gb18030') as f:
            during_mso_9 = False
            for line in f:
                if not during_mso_9 and line.startswith(
                    MSO_9_START
                ):
                    during_mso_9 = True
                    print(1)
                if during_mso_9 and line.rstrip().endswith(
                    MSO_9_END
                ):
                    during_mso_9 = False
                    print(0)
                    continue
                if during_mso_9:
                    continue
                if MSO_9_START in line or MSO_9_END in line:
                    print(line)
                    raise Exception('Error q3490626')
                line = line.replace('gb2312', 'utf-8')
                line = line.replace('“', '"').replace('”', '"')
                tmp.write(line.encode('utf-8'))
        tmp.seek(0)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(tmp, f)
    print('Done. ')

if __name__ == '__main__':
    main()

import time
from datetime import datetime
from pathlib import Path, PurePosixPath

now = time.strftime('%H:%M:%S')
dt_string = datetime.now().strftime("%m/%d/%Y %H:%M")

targetfile1 = PurePosixPath(r'/var/app/current/sampletext.txt') #testing this pureposixpath
f=open(targetfile1,'a',encoding='UTF-8') 
f.write(str(now) + ', ') 
f.write(str(dt_string) + '\n') 

f.close()

print("sampletext_appender.py used [" + dt_string + "]")
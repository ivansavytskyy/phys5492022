# print(len("T220612160813.00,5207.90N,10637.96W,00514.00,08,001.90,1,+024.82,+025.33,+045.08,XX.XXXXXXXX,&BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"))

import datetime as dt
timeString = dt.datetime.utcnow().strftime("%Y%m%d")
print(timeString)
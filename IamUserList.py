import boto3
import datetime
import time
import pandas as pd
import numpy as np
from datetime import date
import pandas as pd
import os
IaM = boto3.client('iam')
todaydate=str(datetime.date.today())
UserList = IaM.list_users()
csvdata=[]
i = 0
while i < len(UserList['Users']):
     iam = boto3.resource('iam')
     user = iam.User(UserList['Users'][i]['UserName'])
     uName = user.name
     pAAth = user.path
     times = str(user.create_date)
     localtime = time.localtime(time.time())
     cyear = int( localtime.tm_year)
     cmonth = int(localtime.tm_mon)
     cday = int(localtime.tm_mday)
     cdate = date(cyear,cmonth,cday)
     month = int(times[5:7])
     day = int(times[8:10])
     ST = date( year , month , day )
     aRn = user.arn
     pLu = user.password_last_used
     uId = user.user_id
     localtime = time.localtime(time.time())
     cyear = int( localtime.tm_year)
     cmonth = int(localtime.tm_mon)
     cday = int(localtime.tm_mday)
     cdate = date(cyear,cmonth,cday)
     diff = cdate - ST
     DiffDays = diff.days
     final_data = [uName,times,pAAth,aRn,pLu,uId,DiffDays]
     csvdata.append(final_data)
     i+=1
df = pd.DataFrame(csvdata, columns=[ "UserName","Creationdate","Path" ,"ARn","PassWordLastUsed","UserId","Age_of_the_user"])
csvname = "IAM Users List data" + "-" + todaydate +".csv"
df.to_csv(csvname)
print ("your file is save in ", os.getcwd()+csvname)




import boto3
import datetime
import time
import pandas as pd
import numpy as np
from datetime import date
import pandas as pd
import os
i = 0
currentregions=[]
while i < len(response['Regions']):
    currentregions.append(response['Regions'][i]['RegionName'])
    i=i+1
csvdata=[]
todaydate=str(datetime.date.today())
for a in currentregions:
    client = boto3.client('elb',region_name = a)
    res = client.describe_load_balancers()
    i = 0
    while i < len(res['LoadBalancerDescriptions']):

            if len(res['LoadBalancerDescriptions'][i]['Instances']) == 0:
				LoadBalancerName = res['LoadBalancerDescriptions'][i]['LoadBalancerName']
				LoadBalancerDnsName = res['LoadBalancerDescriptions'][i]['DNSName']
				LoadBalancerCreatedDate = str(res['LoadBalancerDescriptions'][i]['CreatedTime'])
				RegionOfLoadBalancer = a
				year = int(LoadBalancerCreatedDate[0:4])
				month = int(LoadBalancerCreatedDate[5:7])
				day = int(LoadBalancerCreatedDate[8:10])
				LBDate = date( year , month , day )
				localtime = time.localtime(time.time())
				cyear = int( localtime.tm_year)
				cmonth = int(localtime.tm_mon)
				cday = int(localtime.tm_mday)
				cdate = date(cyear,cmonth,cday)
				diff = cdate - LBDate
				DiffDays = diff.days
				AgeOfLoadBalancer = DiffDays
				FinalData = [ LoadBalancerName,LoadBalancerDnsName , LoadBalancerCreatedDate,RegionOfLoadBalancer,AgeOfLoadBalancer]
				csvdata.append(FinalData)
            i += 1
df = pd.DataFrame(csvdata, columns=[ "LoadBalancerName ","LoadBalancerDnsName" , "LoadBalancerCreatedDate","RegionOfLoadBalancer","AgeOfLoadBalancer"])

csvname = "ListOfELb's With No Instances Attahced " + "-" + todaydate +".csv"
df.to_csv(csvname)
print ("your file is save in ", os.getcwd()+csvname)

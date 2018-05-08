import boto3
import datetime
import time
import pandas as pd
import numpy as np
from datetime import date
import pandas as pd

import botocore.session
"""
ec2 = boto3.client('ec2')
getregions = ec2.describe_regions()
currentregions=[]
k=0
while k < len(getregions['Regions']):
    m=getregions['Regions'][k]['RegionName']
    currentregions.append(m)
    k += 1
print(currentregions)

"""
session = botocore.session.get_session()


currentregions=['ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-east-1','us-west-1', 'us-west-2']
res = []
v=[]
unusedvolid=[]
csvdata=[]
for a in currentregions:
    client = session.create_client('ec2', region_name= a,use_ssl=False)
    response = client.describe_volumes()
    i=0
    while i < len(response['Volumes']):
        q = response['Volumes'][i]['VolumeId']
        ec2 = boto3.resource('ec2',region_name = a)
        volume = ec2.Volume(q)
        if volume.state == "available":
            print(volume)
            p=volume.volume_id
            unusedvolid.append(p)

        #print(q)
        #v.append(q)
        i += 1

for u in unusedvolid:
    volume = ec2.Volume(u)
    times = str(volume.create_time)
    year = int(times[0:4])
    month = int(times[5:7])
    day = int(times[8:10])
    ST = date( year , month , day )
    localtime = time.localtime(time.time())
    cyear = int( localtime.tm_year)
    cmonth = int(localtime.tm_mon)
    cday = int(localtime.tm_mday)
    cdate = date(cyear,cmonth,cday)
    diff = cdate - ST
    DiffDays = diff.days
    volumeid = volume.volume_id
    size = volume.size
    az = volume.availability_zone
    final = [ volumeid,times, DiffDays, az , size ]
    csvdata.append(final)
df = pd.DataFrame(csvdata, columns=['Volumeid','Volume_Created_Date','Age of the Volume from the  current date', 'Availability Zone ' , 'Size In GBs'])
df.to_csv("unusedVolumes_of_an_AWSaccount.csv")

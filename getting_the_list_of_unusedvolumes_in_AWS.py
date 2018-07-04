import boto3
import datetime
import time
import pandas as pd
import numpy as np
from datetime import date
import pandas as pd
import os
client = boto3.client('ec2')

response = client.describe_regions()
i = 0
currentregions=[]
while i < len(response['Regions']):
    currentregions.append(response['Regions'][i]['RegionName'])
    i=i+1


csvdata=[]
todaydate=str(datetime.date.today())
for a in currentregions:
    client = session.create_client('ec2', region_name= a,use_ssl=False)
    response = client.describe_volumes()
    i=0
    while i < len(response['Volumes']):
        q = response['Volumes'][i]['VolumeId']
        ec2 = boto3.resource('ec2',region_name = a)
        volume = ec2.Volume(q)
        if volume.state == "available":
            p=volume.volume_id
            times = str(volume.create_time)
            year = int(times[0:4])
            month = int(times[5:7])
            day = int(times[8:10])
            ST = date( year , month , day )
            volumeid = volume.volume_id
            size = volume.size
            az = volume.availability_zone
            final = [ volumeid,times, DiffDays, az , size ]
            csvdata.append(final)
        i += 1
df = pd.DataFrame(csvdata, columns=['Volumeid','Volume_Created_Date','Age of the Volume from the  current date', 'Availability Zone ' , 'Size In GBs'])
csvname = "ListOfusedVolumesInYourAWSAccOunt" + "-" + todaydate +".csv"
df.to_csv("csvname")

#IF YOU WANT TO DELETE VOLUMES FEW DAYS OLD THEN CHECK THE BELOW PROVIDED LINK .
# https://github.com/Sabihuddin/AWS-PYTHON-SCRIPTS/blob/master/VolumeRetentionScriptForAllRegions.py

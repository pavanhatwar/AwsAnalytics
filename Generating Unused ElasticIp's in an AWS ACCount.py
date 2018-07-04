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
	client = boto3.client('ec2',region_name =a)
    response = client.describe_addresses()
	i = 0
	while i < len(response['Addresses']):
		if "NetworkInterfaceId" not in response['Addresses'][i]:
			print (response['Addresses'][i])
			publicIp = response['Addresses'][i]['PublicIp']
			AllocationId = response['Addresses'][i]['AllocationId']
			Region = a
			FinalData = [publicIp,AllocationId,Region]
			csvdata.append(FinalData)
		i += 1

df = pd.DataFrame(csvdata, columns=[ "PublicIp | (ElasticIp)","AllocationId" ,"Region"])
csvname = "List of unused Elastic Ips  " + "-" + todaydate +".csv"
df.to_csv(csvname)
print ("your file is save in ", os.getcwd()+csvname)

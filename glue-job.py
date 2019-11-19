import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import subprocess
import os
import shutil

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "sampledb", table_name = "user_info_large", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "sampledb", table_name = "user_info_large", transformation_ctx = "datasource0")

print("*******************")
print ("Full record count of user_info:  ", datasource0.count())
print("*******************")

tranches = 10
batch_size=int(datasource0.count()/10)
current_tranche = 0

for batch in range(0,datasource0.count(),batch_size):
    print ("Current tranche is : " + str(current_tranche))
    filteredFrame = Filter.apply(frame = datasource0,
                                  f = lambda x: int(x["user_id"])>=batch_size*current_tranche and int(x["user_id"])<batch_size*(current_tranche+1))
    print ("Filtered record count:  ", filteredFrame.count())
    
    local_directory = "tranche_"+str(current_tranche)
    os.mkdir(local_directory)
    
    dfA = filteredFrame.toDF()
    for row in dfA.collect():
        print(row)
        file_name=local_directory+"/"+row["user_id"]+'.json'
        print("Writing filel:" + file_name)
        f= open(file_name,"w+")
        file_data=json.dumps(row)
        f.write(file_data)
        f.close() 
    
    print("*******************")
    print("Copying " +local_directory + " to s3")
    result = subprocess.run(['aws', 's3', 'cp', '--recursive',local_directory ,'s3://incoming-data-test/user_info/processed/'], stdout=subprocess.PIPE)
    print(result)
    print("*******************")
    shutil.rmtree(local_directory)
    current_tranche = current_tranche +1
    
job.commit()
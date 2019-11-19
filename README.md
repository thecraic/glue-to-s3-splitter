# glue-to-s3-splitter

The glue-to-s3-splitter is an AWS Glue job that implements a specific use case.

A glue data source (in this case an Amazon Athena table), needs to be iterated and a file for each row created in a target S3 bucket.

There are several ways to approach this problem, and parallelizing execution seemed sensible. However tests using PySpark RDD working on each frame produced poor results even with many workers. The maximum throughput achieved reached about 1000 files to S3 per minute. 

To achieve a reasonable run time with a data set of 1M records, it is necessary to approach 10,000 files per minute.

![Overview ](/images/glue-to-s3-splitter_drawio_-_draw_io_app.png)

Testing showed the most effective way to upload a large number of small files to S3 is to bulk copy them with the command line tool. 

This AWS Glue job reads the source table into dynamic frames in tranches, writes the tranche to local disk and bulk copies them to S3. This is done sequentially.

This solution has been tested using 1M rows with 50 full string columns. The data size is 2GB. 

Running time took 2hrs 12 minutes with 10 tranches. This averages approximately 7500 files per minute. By reducing the number of tranches or parallelizing the process the running time could be optimized further.

![Running Time ](/images/Job-runtime.png)

Testing with a Standard AWS Glue worker type did not exercise the driver memory beyond 25%

![Glue Metrics ](/images/AWS_Glue_Console.png)

The data used in the test is available for download here:
[https://s3.amazonaws.com/thecraic.rocks/data.csv](https://s3.amazonaws.com/thecraic.rocks/data.csv)

The DDL for the Athena table is included in this repo.


## Getting Started
* Create an S3 bucket and upload the test [test data](https://s3.amazonaws.com/thecraic.rocks/data.csv).

* Follow the first 2 steps in the [AWS Glue Getting Started](https://docs.aws.amazon.com/glue/latest/dg/getting-started.html) documentation. You now have am AWS Glue Service Policy and Role that can be attached to your jobs. Ensure the role as permission to read and write objects to your S3 bucket.

* Create an Athena Table using the DDL in the file ``athena-table.ddl``. Change the name of the S3 bucket to match your S3 bucket location. The Athena Table will automatically appear in your AWS Glue Catalog and can be used as a datasource in jobs.

* Create a new job and choose the table sampledb.user_info_large as both the data source and target. Do not change any of the settings - all defaults are fine.

* Edit the job script and replace with the contents of the file ``glue-job.py``. **Change the name of the S3 bucket at the end of the script to match your S3 bucket name.

* You can now run the glue job. The output files are placed into the user_info/processed folder. 

![Result ](/images/result.png)


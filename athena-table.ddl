
CREATE EXTERNAL TABLE sampledb.user_info_large (
user_id string , user_data0 string
,user_data1 string
,user_data2 string
,user_data3 string
,user_data4 string
,user_data5 string
,user_data6 string
,user_data7 string
,user_data8 string
,user_data9 string
,user_data10 string
,user_data11 string
,user_data12 string
,user_data13 string
,user_data14 string
,user_data15 string
,user_data16 string
,user_data17 string
,user_data18 string
,user_data19 string
,user_data20 string
,user_data21 string
,user_data22 string
,user_data23 string
,user_data24 string
,user_data25 string
,user_data26 string
,user_data27 string
,user_data28 string
,user_data29 string
,user_data30 string
,user_data31 string
,user_data32 string
,user_data33 string
,user_data34 string
,user_data35 string
,user_data36 string
,user_data37 string
,user_data38 string
,user_data39 string
,user_data40 string
,user_data41 string
,user_data42 string
,user_data43 string
,user_data44 string
,user_data45 string
,user_data46 string
,user_data47 string
,user_data48 string
,user_data49 string
,user_data50 string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   'separatorChar' = ',',
   'quoteChar' = '"',
   'escapeChar' = '\\'
   )
STORED AS TEXTFILE
LOCATION 's3://incoming-data-test/user_info/csv/';
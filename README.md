# asset_data_system

This repo holds helper scripts and config to deploy a "Stock Data Dowloading System"
onto your local linux machine. Each Ticker will have it's own ETL job, which is defined
in a config YML file for each ticker symbol that I want to pull in. There is a helper script 
that reads the configs, and schedules the jobs with the local cron scheduler. There are two 
data sources that we pull stock data from, yFinance (free/dailys) and the IEXCloud 
(not free/intraday). The data is then stored on a local MongoDB instance. We also make sure
to correctly merge the data together, since the ETL jobs run at various times per day; we
don't want duplicates or missing data.


This is a very useful program for trading, however I am considering reworking this
on AWS at some point. Perhaps I can use Cloudformation and deploy the download steps
as AWS Lambda Functions. 

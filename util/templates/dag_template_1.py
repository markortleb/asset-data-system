from pymongo import MongoClient
import yfinance as yf #pip install yfinance
import os
from datetime import datetime, timedelta
import glob
import shutil
import time
import csv

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(
    '{{ dag_name }}',
    default_args=default_args,
    description='ETL to MongoDB table asset_stock_appl_daily.',
    schedule_interval=timedelta(days=1),
)

task_1 = BashOperator(
    task_id = '{{ task_id_1 }}',
    depends_on_past=False,
    bash_command='{{ bash_command_1 }}',
    retries=3,
    dag=dag    
)





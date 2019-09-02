#!/bin/env python3


import tarfile
import os
import boto3
import configparser
import sys
import logging
from datetime import date
from datetime import timedelta
from datetime import datetime
import subprocess
import tarfile
import shutil





# time variables
cur_date = str(date.today())
yes_date = str(date.today() - timedelta(days=1))
cur_time = str(datetime.now())


#function which create a tar archive
def make_tarfile(output_filename, source_dir):
            with tarfile.open(output_filename, "w:gz") as tar:
                    tar.add(source_dir, arcname=os.path.basename(source_dir))

# pusher ( creates a session with AWS) 
def create_client(profile_name):
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')

    return s3_client

# create logger ( for INFO level)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create formatter( used to specify a format of the log file)
formatter = logging.Formatter('%(levelname)s|%(asctime)s|%(name)s|%(message)s|')
file_handler = logging.FileHandler('/var/log/python/python{}.log'.format('backup' + cur_date))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# create logger ( for ERROR level)
logger_er = logging.getLogger(__name__)
logger_er.setLevel(logging.ERROR)

logger_er.addHandler(file_handler)


try:

    if __name__ == '__main__':

        s3 = create_client('default')
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
# Specify the name of your bucket here
        bac = 'name.of.bucket'

        # create archive and check whether a fresh backup exists
        if os.path.exists('/backup-vps/weekly/{}'.format(yes_date)):
            make_tarfile('/root/src/bkup_{}_.tar.gz'.format(yes_date), '/backup-vps/weekly/{}'.format(yes_date))


#upload the tar archive to S3 bucket, and if upload is successfull, remove the local file
            s3.upload_file(f"/root/src/bkup_{yes_date}_.tar.gz", bac, Key = f'backup_{yes_date}')
            response = s3.list_buckets()
            rep = subprocess.check_output(['aws', 's3', 'ls', 'name.of.bucket'])
            if 'backup_{}'.format(yes_date) in rep:
                os.remove(f'/root/src/bkup_{yes_date}_.tar.gz')
                shutil.rmtree(f'/backup-vps/weekly/{yes_date}')
                logger.info("Backup has been completed and pushed successfully.Local files are deleted. Congratz!!!")

        else:
            logger_er.error(f"There is no backup file for {yes_date} date. Do something! I am waiting")


except Exception:
        logger.exception('Something bad has happened.')

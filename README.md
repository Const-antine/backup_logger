# backup_logger
Just a simple script which can be used to push backups to AWS and log any events related to that.

The backups are created by the WHM automatic script. 

You may create a cron job which will run this script on the next day after the back is created. 

Here is my example if CRON job: 0 23 * * 7 /<PathToFile>/backupper.py

Please make sure that you already configured the AWS CLI and required credentials before using the script.

In the script, I was using the "default" profile.

Important: There are the f-strings used in the script. Thus the Python version on your instance should be 3.6 or above.

 

-#!/bin/bash
current_date=`date +"%d-%b-%Y"`
file_location="/home/ubuntu/pull_log/${current_date}.log"

echo `date +"%d-%b-%Y %H:%M"` >> $file_location
cd /home/ubuntu/S21-4910-Project/
echo `git pull` >> $file_location
sudo service apache2 restart
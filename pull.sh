#!/bin/bash

current_date=`date +"%Y-%m-%d %H:%M"`

cd /home/ubuntu/S21-4910-Project/
git_output=`git pull`

log_output="${current_date} ${git_output}"

echo "$log_output" >> /home/ubuntu/pull_script.log

#!/bin/bash
echo `date +"%Y-%m-%d %H:%M"` >> /home/ubuntu/pull_script.log
cd /home/ubuntu/S21-4910-Project/
echo `git pull` >> /home/ubuntu/pull_script.log

#!/bin/bash
# this script check the size of /dev/root and if it occupies more then 90% of the total disk, the clean up action is started

get_root_size=$(df -h | grep /dev/root)

echo $get_root_size

disk_used=$(df -h | grep /dev/root | awk '{ print $5; }')

echo "Disk usage $disk_used "


disk_used="${disk_used%?}"

echo $disk_used

if [ $disk_used -ge 90 ]
then
    echo BIG SIZE DISK SPACE USED
    echo Starting Clean Up process ...
    cd /var/log/
    sudo rm -R ./journal
    sudo rm ./syslog.*
    sudo rm ./user.log.*
    sudo rm ./messages.*
    sudo rm ./daemon.log.*

    cd /home/pi/.vscode-server
    sudo rm -R ./cli
    sudo rm ./.cli*
    sudo rm ./code*
    sudo rm -R ./data
else
   echo there is enough disk space
fi

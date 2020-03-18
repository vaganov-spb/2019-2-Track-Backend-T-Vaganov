#!/usr/bin/env bash

. backup.config

top_level_backup_dir=/var/backups/pg

cd "$top_level_backup_dir" || exit 1

backup_date=$( date +%Y-%m-%d_At_%H:%M:%S)

pg_dumpall -r > roles.dump

pg_dump -Fc -f /var/backups/pg/"backup-$backup_date.dump" quack_db

COPY_COUNTER=`find . -type f | grep "backup" | wc -l`

if [ $COPY_COUNTER -gt $ROTATION_NUM ]
then 

NEED_TO_DELETE_COUNTER=$(($COPY_COUNTER-$ROTATION_NUM))

for (( i==1; i<$NEED_TO_DELETE_COUNTER; i++ ))
do

rm -f ./$(ls -l | grep "backup" | sort | head -n 1)

done
fi

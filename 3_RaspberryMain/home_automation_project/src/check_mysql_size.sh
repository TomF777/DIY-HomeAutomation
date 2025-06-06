#!/bin/bash

# script iterates through all tables in database 'db_home_automation' and check its size. 
# If size greater then 20 Mb it starts to reduce the size by deleting first 100 rows.   

# test how to call sql query
#mysql -u mysql_user -pInternet1!  -D db_home_automation -e "SELECT * FROM room_living ORDER BY Timestamp DESC LIMIT 1"

# list size of all tables in 'db_home_automation' database
mysql -u mysql_user -pInternet1!  -D db_home_automation -e "SELECT TABLE_NAME AS 'Table', ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024) AS 'Size (MB)' 
											FROM information_schema.TABLES 
											WHERE TABLE_SCHEMA = 'db_home_automation' 
											ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;"


# get size of 'room_living' table
# result=$(mysql -u mysql_user -pInternet1!  -D db_home_automation -e "SELECT TABLE_NAME AS 'Table', ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024) AS 'Size (MB)'
# 												   FROM information_schema.TABLES
# 												   WHERE TABLE_SCHEMA = 'db_home_automation' AND TABLE_NAME = 'room_living'
# 												   ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;")



# echo $result
echo "-------------------------------------------------------------------------"

# check DB size of generic_outside_particulate_matter
check_table_size () {
	# global variables result and size
	result=$(mysql -u mysql_user -pInternet1!  -D db_home_automation -e "SELECT TABLE_NAME AS 'Table', ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024) AS 'Size (MB)'
                                                                                                   FROM information_schema.TABLES
                                                                                                   WHERE TABLE_SCHEMA = 'db_home_automation' AND TABLE_NAME = '$1'
                                                                                                   ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;")

	size=$( echo $result | awk '{print $5}')

}

# list with all tables in database
test_table="room_kitchen generic_outside_particulate_matter \
			room_bedroom room_bathroom generic_outside_conditions \
			generic_current_integral room_bathroom_zigbee \
			room_kitchen_zigbee room_living"

# iterate through all tables and check its size in MB
for table in $test_table; do 
	# result=$(mysql -u mysql_user -pInternet1!  -D db_home_automation -e "SELECT TABLE_NAME AS 'Table', ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024) AS 'Size (MB)'
    #                                                                                                FROM information_schema.TABLES
    #                                                                                                WHERE TABLE_SCHEMA = 'db_home_automation' AND TABLE_NAME = '${table}'
    #                                                                                                ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;")

	check_table_size $table 
	# test1=$( echo $result | awk '{print $5}')
	# test2=$( echo $result | cut -d ' ' -f 5)

	# size=$( echo $result | awk '{print $5}')
	echo Table: $table size: $size MB

	while [ $size -ge 20 ]
		do
			echo DB is too big... reducing its size...
			# delete first 100 rows
			mysql -u mysql_user -pInternet1!  -D db_home_automation -e "DELETE FROM db_home_automation.${table} ORDER BY 'Timestamp' ASC limit 100"
			sleep 2
			check_table_size $table
			echo Table: $table size: $size MB
		done

	echo "******************************************************************"

done




#/bin/bash
PRENUMBER=""
COUNT=1;
RUN=0;
echo "" > /tmp/getDownGoing.tmp
for number in $(curl -s http://www.aastocks.com/en/LTP/RTAI.aspx?type=2 | grep "[0-9][0-9][0-9][0-9][0-9]\.HK"   |awk '{print $1}' |cut -c1-5 |sort)
do
	if [ "$RUN" -eq "0" ] 
	then 
	    PRENUMBER=$number;
        else
		if [ "$PRENUMBER" -eq "$number" ] ;
		then
			COUNT=$((COUNT+1))		
		else
			echo $COUNT $PRENUMBER >> /tmp/getDownGoing.tmp
			PRENUMBER=$number;
			COUNT=1;
		fi
	fi
	RUN=$((RUN+1))
done

cat /tmp/getDownGoing.tmp | sed '/^\s*$/d' |sort -r >$1/$(date +%Y%h%d)D.txt
rm /tmp/getDownGoing.tmp
/home/apoletics_compute/HKStockAnalysis/getai.py -l 0 -f "$1/$(date +%Y%h%d)D.txt"  -s $2 -r $3 -p $4

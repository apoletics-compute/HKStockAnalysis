#/bin/bash
PRENUMBER=""
COUNT=1;
RUN=0;
echo "" > /tmp/getUpRunning.tmp
for number in $(curl -s http://www.aastocks.com/en/LTP/RTAI.aspx?type=1 | grep "[0-9][0-9][0-9][0-9][0-9]\.HK"   |awk '{print $1}' |cut -c1-5 |sort)
do
	if [ "$RUN" -eq "0" ] 
	then 
	    PRENUMBER=$number;
        else
		if [ "$PRENUMBER" -eq "$number" ] ;
		then
			COUNT=$((COUNT+1))		
		else
			echo $COUNT $PRENUMBER >> /tmp/getUpRunning.tmp
			PRENUMBER=$number;
			COUNT=1;
		fi
	fi
	RUN=$((RUN+1))
done

cat /tmp/getUpRunning.tmp |sort -r
rm /tmp/getUpRunning.tmp

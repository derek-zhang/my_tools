 #!/bin/sh
 
 i=0
 
 echo > /root/log
 
 #if [ -f /opt/WCG/bin/content_line ]; then
 #/opt/WCG/bin/content_line -s proxy.config.diags.debug.enabled -v 1
 #/opt/WCG/bin/content_line -s proxy.config.diags.debug.tags -v http_cs
 #/opt/WCG/bin/content_line -x
 #fi
 
 while [ $i -le 500 ]; do
 
 tm=`date`
 
 echo "---------------- $tm ---------------------" >> /root/log
 
 top -b -d 1 -n 1 | head -n 25 >> /root/log
 
 /root/net_state.pl >> /root/log
 
 gstack `pidof content_gateway` >> /root/log
 
 echo "-------------------------------------------------------------" >> /root/log
 
 echo >> /root/log
 
 i=$(($i+1))
 
 sleep 1
 
 done;
 
 
 #if [ -f /opt/WCG/bin/content_line ]; then
 #/opt/WCG/bin/content_line -s proxy.config.diags.debug.enabled -v 0
 #/opt/WCG/bin/content_line -s proxy.config.diags.debug.tags -v NULL
 #/opt/WCG/bin/content_line -x
 #fi
 
 day=`date | awk -F' ' '{printf $2 $3}'`
 
 cp -f /root/log /root/log.$day

#!/usr/bin/env bash

# OpenSSL requires the port number.
SERVER=10.231.41.26:12345
DELAY=1
ciphers=$(openssl ciphers 'ALL:eNULL' | sed -e 's/:/ /g')

echo Obtaining cipher list from $(openssl version).

for cipher in ${ciphers[@]}
do
echo -n Testing $cipher...
result=$(echo -n | openssl s_client -cipher "$cipher" -connect $SERVER 2>&1)
if [[ "$result" =~ "Cipher :" ]] ; then
    echo YES
else
    if [[ "$result" =~ ":error:" ]] ; then
       error=$(echo -n $result | cut -d':' -f6)
       echo NO \($error\)
    else
      echo UNKNOWN RESPONSE
      echo $result
    fi
fi
sleep $DELAY
done


# 测试服务器所支持的cipher list
# if [[ "$result" =~ "Cipher :" ]] 这句话可能要根据openssl不同版本修改，比如"Cipher is"
#http://superuser.com/questions/109213/is-there-a-tool-that-can-test-what-ssl-tls-cipher-suites-a-particular-website-of

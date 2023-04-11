#!/bin/bash

if [ $# -lt 1 ]; then
	echo "#(nodes) is required.";
	exit 1;
fi
if [ $1 -eq 4 ];then
	outputFile="testRing4Result.txt"
fi
if [ $1 -eq 6 ];then
	outputFile="testRing6Result.txt"
fi
if [ $1 -eq 8 ];then
	outputFile="testRing8Result.txt"
fi

echo "=============$outputFile=============";
for i in `seq 1 $1`; do
	echo "NODE b$i dumps:";
	# cat b$i-output.txt | grep "INFO"
	# cat b$i-output.txt | grep -v "DEBUG";
	cat b$i-output.txt | grep "INFO" | tee -a $outputFile;
	echo "";
done

#!/bin/sh
echo Running on host `hostname`
echo Start Time is `date`
echo Directory is `pwd`
echo Working directory is `pwd` 

../../../sim-outorder -config simconfig art00.peak.ev6 -scanfile c756hel.in -trainfile1 a10.img -trainfile2 hc.img -stride 2 -startx 110 -starty 200 -endx 160 -endy 240 -objects 10 &>../../results/cfp/art.txt 
echo End Time is `date`


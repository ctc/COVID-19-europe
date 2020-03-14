#!/bin/sh

DIR=`dirname "$0"`

. ${DIR}/config.sh



cd ${WORK_DIR}
/usr/bin/git clone https://github.com/CSSEGISandData/COVID-19.git

cd ${WORK_DIR}/COVID-19
/usr/bin/git pull

cd ${WORK_DIR}/scripts
${WORK_DIR}/scripts/reformat.py ${WORK_DIR}

cd ${WORK_DIR}
/usr/bin/git add total_confirmed.csv
/usr/bin/git add total_deaths.csv
/usr/bin/git add total_recovered.csv

/usr/bin/git add total_grow_percent_confirmed.csv
/usr/bin/git add total_grow_percent_deaths.csv
/usr/bin/git add total_grow_percent_recovered.csv

/usr/bin/git add by_population_confirmed.csv
/usr/bin/git add by_population_deaths.csv
/usr/bin/git add by_population_recovered.csv

/usr/bin/git add by_population_grow_percent_confirmed.csv
/usr/bin/git add by_population_grow_percent_deaths.csv
/usr/bin/git add by_population_grow_percent_recovered.csv

/usr/bin/git add austria.csv


DATE=`date`
/usr/bin/git commit -m "${DATE}"
/usr/bin/git push



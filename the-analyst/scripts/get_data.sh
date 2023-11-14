#!/bin/bash

FMT='+%Y%m%d'
ST_DT='20200101'
EN_DT='20231107'
i="$ST_DT"
PAIRS="BTC/EUR ETH/EUR"
EXCHANGE="binance"

while [[ $(date $FMT -d $i) -le $EN_DT ]]; do
	e=$(date $FMT -d "$i +1 month")
  echo "---> $i-$e"
	docker compose run --rm freqtrade download-data --pairs $PAIRS --exchange $EXCHANGE --timerange $i-$e
	docker compose stop
  sleep 60
  i=$e
done

#/bin/bash

if [ $1 = "sample" ]; then
    docker compose up
fi

if [ $1 = "data" ]; then
    docker compose run \
        --rm freqtrade download-data \
        --pairs BTC/EUR ETH/EUR \
        --exchange bitstamp \
        --pairs BTC/EUR \
        --timerange 20231001-20231007
fi

if [ $1 = "ai" ]; then
    docker-compose run \
        --rm freqtrade trade \
        --config model-v1/config.json \
        --strategy FreqaiExampleStrategy \
        --freqaimodel LightGBMRegressor
fi


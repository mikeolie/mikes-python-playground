#!/bin/sh

curl -X GET https://s3.amazonaws.com/ccg-corporate-production/reports/NGC/CoinRep.zip >current_coins.zip

# unzip zip file and get csv
unzip -d ./ "$PWD/current_coins.zip"
# turn csv into json
mv "$PWD/CoinRep.txt" "$PWD/CoinRep.csv"

rm current_coins.zip

echo "Converting into json..."
python csv_to_json.py

# done
echo "Done!"

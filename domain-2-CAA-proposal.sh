#!/bin/bash

if [ -z $1 ]; then
    echo "Error: please use an domain as input for this."
    exit 1
fi


curl "https://certspotter.com/api/v0/certs?expired=false&duplicate=false&domain=$1" | \
    grep issuer | \
    sort -u | \
    while read LINE; do 
        #echo "$LINE" | tr '[:upper:]' '[:lower:]'
        LOWER=$(echo "$LINE" | tr '[:upper:]' '[:lower:]')

        if [[ $LOWER = *"globalsign"* ]]; then
            echo "CAA 0 issue \"globalsign.com\""
            echo "CAA 0 issuewild \"globalsign.com\""
            continue
        elif [[ $LOWER = *"pkioverheid"* ]]; then
            echo "CAA 0 issue \"pkioverheid.nl\""
            echo "CAA 0 issue \"logius.nl\""
            continue
        elif [[ $LOWER = *"digicert"* ]]; then
            echo "CAA 0 issue \"digicert.com\""
            echo "CAA 0 issuewild \"digicert.com\""
            continue
        elif [[ $LOWER = *"thawte"* ]]; then
            echo "CAA 0 issue \"thawte.com\""
            echo "CAA 0 issuewild \"thawte.com\""
            continue
        elif [[ $LOWER = *"geotrust"* ]]; then
            echo "CAA 0 issue \"geotrust.com\""
            echo "CAA 0 issuewild \"geotrust.com\""
            continue
        elif [[ $LOWER = *"comodo"* ]]; then
            echo "CAA 0 issue \"comodoca.com\""
            echo "CAA 0 issuewild \"comodoca.com\""
            continue
        fi
    done


exit 0




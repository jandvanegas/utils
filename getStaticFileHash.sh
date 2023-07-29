curl -s $1 | openssl dgst -sha384 -binary | openssl base64 -A

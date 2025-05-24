#!/bin/bash

# Define a temporary, consistent image name
IMAGE_NAME=nostr-signal-filter-tinyurl

# 1. Build image if it doesn't exist
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "Building Docker image: $IMAGE_NAME"
    docker build -t $IMAGE_NAME .
fi

# If argument is provided
if [[ -n "$1" ]]; then
    docker run --rm $IMAGE_NAME shorten_links_in_text.py "$1"

# If data is piped into the script
elif ! [ -t 0 ]; then
    docker run --rm -i $IMAGE_NAME shorten_links_in_text.py < /dev/stdin

# If no input, show usage
else
    echo "Usage:"
    echo "  echo 'https://example.com' | $0"
    echo "  $0 'https://example.com'"
    exit 1
fi


#!/bin/bash

# CD into the directory of the script
cd "$(dirname "$0")"

# Load environment variables
source .env

# Get current year and day of month in UTC-5 which is when the puzzle drops
# + 1 minute just to make sure it's the right day
YEAR=$(date -u -d "-5 hours +1 minute" +"%Y")
DAY=$(date -u -d "-5 hours +1 minute" +"%d")

# If DAY is less than 10, remove the leading 0
if [[ $DAY == 0* ]]; then
  DAY_NO_ZERO=${DAY:1}
fi

# Get input for the day
echo "Getting input for $YEAR day $DAY_NO_ZERO"
curl -s https://adventofcode.com/$YEAR/day/$DAY_NO_ZERO/input --cookie "session=$SESSION" > ./$YEAR/day$DAY/input.txt
echo "Done! Placed input in $YEAR/day$DAY/input.txt"

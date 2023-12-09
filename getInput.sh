#!/bin/bash

# CD into the directory of the script
cd "$(dirname "$0")"

# Load environment variables
source .env

# Check if SESSION is set
if [ -z "$SESSION" ]; then
  echo "SESSION is not set. Please set it in .env"
  exit 1
fi

# Get current year and day of month in UTC-5 which is when the puzzle drops
# + 1 minute just to make sure it's the right day
YEAR=$(date -u -d "-5 hours +1 minute" +"%Y")
MONTH=$(date -u -d "-5 hours +1 minute" +"%m")
DAY=$(date -u -d "-5 hours +1 minute" +"%d")

# Check that the month and day is between Dec 1 and Dec 25
if [ $# -eq 0 ]; then
  if [ $MONTH -ne 12 ] || [ $DAY -lt 1 ] || [ $DAY -gt 25 ]; then
    echo "It's not December yet, please wait until December 1st"
    exit 1
  fi
fi

# If args for year and day are passed, use those
# -d is for day and -y is for year
# For other flags, echo error
while getopts d:y: option; do
  case "${option}" in
  d)
    DAY=$OPTARG
    ;;
  y)
    YEAR=$OPTARG
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    exit 1
    ;;
  esac
done

# Check that year is an integer
if ! [[ $YEAR =~ ^[0-9]+$ ]]; then
  echo "Year is not an integer"
  exit 1
fi

# Check that day is an integer
if ! [[ $DAY =~ ^[0-9]+$ ]]; then
  echo "Day is not an integer"
  exit 1
fi

# If DAY is less than 10, store day without the leading 0
# If doesn't have leading 0, add it
if [[ $DAY == 0* ]]; then
  DAY_NO_ZERO=${DAY:1}
else
  DAY_NO_ZERO=$DAY
  if [ $DAY -lt 10 ]; then
    DAY="0$DAY"
  fi
fi

# Check if the directory for the year exists
if [ ! -d "$YEAR" ]; then
  echo "Creating directory for year $YEAR"
  mkdir $YEAR
fi

# Check if the directory for the day exists, make duplicate of template2 if not
if [ ! -d "$YEAR/day$DAY" ]; then
  echo "Creating directory for day $DAY"
  cp -r template2 $YEAR/day$DAY
fi

# Get input for the day
echo "Getting input for $YEAR day $DAY_NO_ZERO from https://adventofcode.com/$YEAR/day/$DAY_NO_ZERO/input"
curl -s https://adventofcode.com/$YEAR/day/$DAY_NO_ZERO/input --cookie "session=$SESSION" >./$YEAR/day$DAY/input.txt
echo "Done! Placed input in $YEAR/day$DAY/input.txt"

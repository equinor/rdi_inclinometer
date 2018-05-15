#! /bin/bash

#
# trim-img.sh - Trim the size of an Raspberry PI img file (mac osx)
#
#   Requirements:   Install truncate via brew
#
#       1 - ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
#       2 - brew install truncate
#
# The script is taken from https://gist.github.com/jtanderson312/a21924fa3ce9505f08ae6caf605fba7c
#

# Check number of args
if [ "$#" -ne 1 ]
then
    echo "$0: Usage: $0 imagename" >&2
    exit 10
fi
IMAGE="$1"


# Make sure the image is a file
if [ ! -f "$IMAGE" ]
then
    echo "$0: '$IMAGE' is not a valid image name." >&2
    exit 1
fi

LAST_START=0
LAST_SIZE=0
PARTITION_DATA=$(fdisk -d $IMAGE)

while IFS= read -r line
do
    START=$(echo $line | awk -F  "," '/1/ {print $1}')
    SIZE=$(echo $line | awk -F  "," '/1/ {print $2}')
    if ((START > LAST_START))
    then
        LAST_START=$START
        LAST_SIZE=$SIZE
    fi
done <<< "$PARTITION_DATA"

#echo "$LAST_START / $LAST_SIZE"
SECTOR_SIZE=512
PARTITION_END=$((LAST_START + LAST_SIZE))
PARTITION_OFFSET=$((PARTITION_END*SECTOR_SIZE))


#echo $PARTITION_END / $PARTITION_OFFSET

# Output Information read
echo "    Sector size: ${SECTOR_SIZE} (bytes)"
echo "    Last partition end: ${LAST_SIZE} (sectors)"
echo "    New size: ${PARTITION_OFFSET} (bytes)"    
    
echo "* Resizing image..."
truncate $IMAGE -s $PARTITION_OFFSET

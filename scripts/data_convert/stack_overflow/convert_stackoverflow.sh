#!/bin/bash
. scripts/common_proc.sh

input="$1"

if [ "$input" = "" ] ; then
  echo "Specify input file (1st arg)"
  exit 1
fi

interm="$2"

if [ "$interm" = "" ] ; then
  echo "Specify intermediate file prefix (2d arg)"
  exit 1
fi

output="$3"

if [ "$output" = "" ] ; then
  echo "Specify output file (3d arg)"
  exit 1
fi

# Do it only after argument parsing
set -eo pipefail

target/appassembler/bin/ConvertStackOverflowStep1 -input "$input" -output "${interm}1"

sort -k 1,1 -n -s "${interm}1" > "${interm}2"

target/appassembler/bin/ConvertStackOverflowStep2 -input "${interm}2" -output "$output" -exclude_code

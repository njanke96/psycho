#!/bin/bash

# Example startscript (bash shells)

export TWILIO_SID=YOUR_SID_HERE
export TWILIO_TOKEN=YOUR_TOKEN_HERE

# optional
#export PSYCHO_NUMBER = YOUR_PHONE_NUMBER
#export PSYCHO_TARGET = DESTINATION_PHONE_NUMBER

python psycho.py

# PSYCHO

Simple twilio phone number proxy..  

It's a script using twilio to send sms as someone else, in case you don't want to reveal your phone number, or are blocked.

## Setting up

#### Twilio

1. Make a twilio account (can't be a free trial).
2. Create ONE messaging service with no inbound request config.
3. Create as many phone numbers as you want, assign the sms behavior to your messaging service.
4. Get your SID and private api key.

#### The script

TODO: windows batch script

1. Clone or download the repo.
2. CD to the directory in a terminal.
3. `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`
4. Modify the values in start.sh or start.bat. If you leave the optional values commented you will be prompted for these when you run the script.

## Usage

Start the script with `bash start.sh` or `start.bat` and enjoy. Text the number listed after 'Using twilio number' from your phone to have your messages forwarded to the target phone number. Ctrl+C will cause the program to ask if you would like to use a new number. The next unused number on your account will be used.

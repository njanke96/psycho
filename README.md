# PSYCHO

The perfect python script for the psycho ex-girlfriend.  

It's a script using twilio to send messages as someone else, in case he (or she) has blocked your number. I made this to learn the twilio api.

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
4. Modify the values in start.sh. If you leave the optional values commented you will be prompted for these when you run the script.

## Usage

Start the script with `bash start.sh` and enjoy. Text the number listed after 'Using twilio number' from your phone to have your messages forwarded to the target phone number. Ctrl+C will cause the program to ask if you would like to use a new number. The next unused number on your account will be used.

## Sample output

```
Target: +11234567890
Using twilio number: +16131122233
Forwarded "Hey bb it's me" from <+12501234567> to <+11234567890>
Forwarded "You're crazy, I'm calling the police" from <+11234567890> to <+12501234567>
Forwarded "Don't you love me anymore?" from <+12501234567> to <+11234567890>
```

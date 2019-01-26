import urllib3
from requests import get, post, delete
from requests.auth import HTTPBasicAuth
from os import environ
from time import sleep

# constants
TWILIO_BASE = 'https://api.twilio.com/2010-04-01'
TWILIO_BASE_SERVICES = 'https://messaging.twilio.com/v1'
TWILIO_SID = environ['TWILIO_SID']
TWILIO_TOKEN = environ['TWILIO_TOKEN']
RQ_AUTH = HTTPBasicAuth(TWILIO_SID, TWILIO_TOKEN)

def main():
    used_nums = []

    # prompt the destination number if it wasn't specified as an environment var
    try:
        source_num = environ['PSYCHO_NUMBER']
    except KeyError:
        source_num = input('Enter your phone number: ')

    # prompt the destination number if it wasn't specified as an environment var
    try:
        dest_num = environ['PSYCHO_TARGET']
    except KeyError:
        dest_num = input('Enter the destination phone number: ')

    if not source_num.startswith('+') or not dest_num.startswith('+'):
        fail('Please use the proper phone number format, example: +12501234567')

    # main loop
    print('Target: {}'.format(dest_num))
    main_loop(source_num, dest_num, used_nums)
    

def main_loop(source_num, dest_num, used_nums):
    try:
        # get a phone number
        current_num = new_twilio_number(used_nums)
        print('Using twilio number: {}'.format(current_num))

        while True:
            get_messages_url = '{}/Accounts/{}/Messages.json?From={}'

            # check messages from the target
            from_num = '%2B' + dest_num[1:]
            msgs = get_with_auth(get_messages_url.format(
                                 TWILIO_BASE, TWILIO_SID, from_num))
            
            # we only care about page 1 since we remove msgs after reading them
            if get_msg_response_condition(msgs):
                continue

            msgs = msgs['messages']

            # forward messages from our target to the user
            process_messages(msgs, current_num, source_num)
            
            # check messages from our user
            from_num = '%2B' + source_num[1:]
            msgs = get_with_auth(get_messages_url.format(
                                 TWILIO_BASE, TWILIO_SID, from_num))

            if get_msg_response_condition(msgs):
                continue 

            msgs = msgs['messages']

            # descreetly forward messages from our user to the target
            process_messages(msgs, current_num, dest_num, True)

            # check outgoing messages from twilio
            from_num = '%2B' + current_num[1:]
            msgs = get_with_auth(get_messages_url.format(
                                 TWILIO_BASE, TWILIO_SID, from_num))

            if get_msg_response_condition(msgs):
                continue

            msgs = msgs['messages']
            for msg in msgs:
                # process twilio's outbound messages
                if msg['direction'] != 'inbound':
                    if msg['status'] not in ['accepted', 'queued', 'sending', 'receiving']:
                        delete_with_auth('{}/Accounts/{}/Messages/{}.json'.format(
                            TWILIO_BASE, TWILIO_SID, msg['sid']))

            # prevent bullshit
            sleep(0.5)
    except KeyboardInterrupt:
        yn = input('\nChange phone number and continue? [y/n]')
        if yn.lower() == 'y':
            main_loop(source_num, dest_num, used_nums)
        else:
            exit(0)

def get_msg_response_condition(msgs):
    return msgs is None or 'messages' not in msgs

# Http Helper functions

def get_with_auth(url):
    return get(url, auth=RQ_AUTH).json()

def post_data_with_auth(url, args):
    return post(url, auth=RQ_AUTH, data=args)

def delete_with_auth(url):
    return delete(url, auth=RQ_AUTH).status_code

##

def process_messages(msgs, from_num, to_num, discreet=False):
    for msg in msgs:
        # ignore outbound messages, they should never be here though
        if msg['direction'] != 'inbound':
            continue

        # forward incomming
        if not discreet:
            prefix = 'Forwarded from {}: '.format(msg['from'])
        else:
            prefix = ''

        forward_body = '{}{}'.format(prefix, msg['body'])
        post_data_with_auth(
            '{}/Accounts/{}/Messages.json'.format(
                TWILIO_BASE, TWILIO_SID),
            {'From': from_num, 'Body': forward_body, 'To': to_num}
        )

        # delete it
        delete_with_auth('{}/Accounts/{}/Messages/{}.json'.format(
            TWILIO_BASE, TWILIO_SID, msg['sid']))

        # log it
        print('Forwarded "{}" from <{}> to <{}>'.format(msg['body'], msg['from'], to_num))


def new_twilio_number(used_nums):
    """
    Fetch an unused number from twilio
    """

    # fetch all services
    services = get_with_auth('{}/Services'.format(TWILIO_BASE_SERVICES))
    if services is None or 'services' not in services:
        fail('Failed to retrieve services.')

    services = services['services']

    # use the first service
    if services:
        service = services[0]
    else:
        fail('Your account has no services')

    # fetch a phone number
    phone_nums = get_with_auth(service['links']['phone_numbers'])

    if phone_nums is None or 'phone_numbers' not in phone_nums:
        fail('Failed to retrieve phone numbers.')

    phone_nums = phone_nums['phone_numbers']

    # use the first unused phone number
    for x in phone_nums:
        num = x['phone_number']
        if num not in used_nums:
            used_nums.append(num)
            return num

    fail('No more phone numbers we can use. Consider buying another phone number, ' + 
         'but ask yourself first "is he really worth it?".')

def fail(message=''):
    """
    Fail with a message
    """
    if message:
        print(message)

    exit(-1)

if __name__ == '__main__':
    main()

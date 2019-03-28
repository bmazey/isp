import json
import os
import dateutil.parser
import time
from botocore.vendored import requests


""" Here is our main AWS LF1 implementation  - some functions are omitted as they contain API keys """


# use dateutil to check if user's date input can be correctly parsed ...
def is_valid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


# check if user input can be cast to an integer
def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def refer(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# helper function to get Lex intent slots
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


# close session when done
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


# helper function to expose validation results
def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def ask_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


# respond to initial greeting
def greeting_intent():
    return {
        'dialogAction': {
            "type": "ElicitIntent",
            'message': {
                'contentType': 'PlainText',
                'content': 'Hello! My name is Higgins - how can I help you?'}
        }
    }


# validate user input
# only implementing NYC locations for now ...
def validate_user_input(location, cuisine, num_people, date, time):
    # validate locations
    locations = ['brooklyn', 'queens', 'new york', 'manhattan', 'the bronx', 'staten island']
    if location is not None and location.lower() not in locations:
        return build_validation_result(False,
                                       'Location',
                                       'Please provide your desired location!')

    # validate cuisines
    cuisines = ['japanese', 'korean', 'indian', 'italian', 'mexican']
    if cuisine is not None and cuisine.lower() not in cuisines:
        return build_validation_result(False,
                                       'Cuisine',
                                       'Please provide your desired cuisine!')

    # validate party size
    if num_people is not None:
        num_people = int(num_people)
        if num_people > 20 or num_people < 0:
            return build_validation_result(False,
                                           'People',
                                           'Please provide the size of your party (20 people max)!')

    return build_validation_result(True, None, None)


def restaurant_intent(intent_request):
    # start by getting all intents
    location = get_slots(intent_request)["Location"]
    cuisine = get_slots(intent_request)["Cuisine"]
    date = get_slots(intent_request)["Date"]
    time = get_slots(intent_request)["Time"]
    num_people = get_slots(intent_request)["People"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)

        validation_result = validate_user_input(location, cuisine, num_people, date, time)

        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return ask_slot(intent_request['sessionAttributes'],
                            intent_request['currentIntent']['name'],
                            slots,
                            validation_result['violatedSlot'],
                            validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                               'sessionAttributes'] is not None else {}

        return refer(output_session_attributes, get_slots(intent_request))

    # Add Yelp API endpoint to get the data
    requestData = {
        "term": cuisine + ", restaurants",
        "location": location,
        "categories": cuisine,
        "limit": "4",
        "peoplenum": num_people,
        "Date": date,
        "Time": time
    }

    resultData = invoke_yelp_api(requestData)

    # resultData = ''
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': resultData})


# function to call Yelp API GET
def invoke_yelp_api(requestData):

    # base url
    url = "https://api.yelp.com/v3/businesses/search"
    querystring = requestData
    payload = ""

    # using API key in Bearer header
    headers = {
        'Authorization': "Bearer wdT6xFqtJXQ9LELu-mp6PsUa_RTysWMHb2dkoDqahQCsTGelJTy5hkwBn05lIQ55C6BpjF6NRgx5bGE9EKPDlBiNqI3hnYEIAnddd4cdv-H590iKnMFCoSryAYONXHYx",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    message = json.loads(response.text)

    if len(message['businesses']) < 0:
        return 'Hmmm ... I can\'t seem to find any restaurants matching your criteria.'

    text = "For " + requestData['categories'] + " food on " + requestData['Date'] + " at " + requestData['Time']\
        + " I recommend: "
    count = 1
    for business in message['businesses']:
        text = text + " " + str(count) + "." + business['name'] + ", located at " + business['location'][
            'address1'] + " "
        count += 1

    text = text + 'for your party of ' + requestData['peoplenum'] + '!'

    return text


def action_intent(intent_request):
    # this method identifies the intent using lex SDK and calls the matching method
    intent = intent_request['currentIntent']['name']

    if intent == 'GreetingIntent':
        return greeting_intent()
    elif intent == 'RestaurantIntent':
        return restaurant_intent(intent_request)
    else:
        print('Unidentifiable intent: ' + str(intent))


def handler(event, context):
    """ This is our main handler function for LF1 AWS Lambda """
    return action_intent(event)

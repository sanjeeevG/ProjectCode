import logging
import pandas as pd

from lex_utils import elicit_slot, delegate, close, ElicitAction, DelegateAction
#from utils import validate_dialog, init_or_load_session, finalize_session, actually_book_the_hotel
from welcomeintent import *
from appointmentintent import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logging.debug(event)
    botName = getBotName(event)
    intent_name = getIntentName(event)

    logger.debug('event.bot.name=%s', botName)
    #logger.debug('userId=%s, intentName=%s', event['userId'], intent_name)
    logger.debug('intentName=%s', intent_name)

    if intent_name.lower() == 'appointmenthandler':
        return appointment_handler(event)
    elif intent_name.lower() == 'welcome':
        return welcome_handler(event)
    else:
        raise Exception('Intent with name %s not supported' % intent_name)

# Get Bot Name


def getBotName(event):
    return event['bot']['name']

# Get Intent Name


def getIntentName(event):
    return event['sessionState']['intent']['name']

# Get Session attributes


def getSessionAttributes(event):
    sessionState = event['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}

# Get Slots


def getSlots(event):
    return event['sessionState']['intent']['slots']

# Get Slot


def getSlot(event, slotName):
    slots = getSlots(event)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        logger.debug('resolvedValue={}'.format(
            slots[slotName]['value']['resolvedValues']))
        return slots[slotName]['value']['resolvedValues']
    else:
        return None


def elicit_slot(session_attributes, intent_request, slots, slot_to_elicit, slot_elicitation_style, message):
    return {'sessionState': {'dialogAction': {'type': 'ElicitSlot',  'slotToElicit': slot_to_elicit,  'slotElicitationStyle': slot_elicitation_style},
            'intent': {'name': intent_request['sessionState']['intent']['name'],
                       'slots': slots,
                       'state': 'InProgress'
                       },
            'sessionAttributes': session_attributes,
            'originatingRequestId': 'REQUESTID'
    },
        'sessionId': intent_request['sessionId'],
        'messages': [message],
        'requestAttributes': intent_request['requestAttributes']
        if 'requestAttributes' in intent_request else None
    }

#Build Validation result


def build_validation_result(isvalid, violated_slot, slot_elicitation_style,  message_content):
    return {'isValid': isvalid,
            'violatedSlot': violated_slot,
            'slotElicitationStyle': slot_elicitation_style,
            'message': {'contentType': 'PlainText',
                        'content': message_content}
            }


def close(event, session_attributes, fulfillment_state, message):
    event['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': event['sessionState']['intent'],
            'originatingRequestId': 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
        },
        'messages': [message],
        'sessionId': event['sessionId'],
        'requestAttributes': event['requestAttributes'] if 'requestAttributes' in event else None
    }


def closeWithOptions(event, session_attributes, fulfillment_state, message, message2):
    event['sessionState']['intent']['state'] = fulfillment_state

    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ConfirmIntent'
            },
            'intent': event['sessionState']['intent'],
            'originatingRequestId': 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
        },
        'messages': [message, message2],
        'sessionId': event['sessionId'],
        'requestAttributes': event['requestAttributes'] if 'requestAttributes' in event else None,
    }


def welcome_handler(event):
    slots = getSlots(event)
    name = getIntentName(event)
    phoneNo = getSlot(event, 'phoneNo')

    logger.debug('Debug =%s', phoneNo)

    drInfo = getDoctorInfo(phoneNo)

    message = 'Sorry, I couldn''t recognise you.'\
        'May I suggest you registering with Federate Health.'
    if drInfo != "None":
        message = f"Hello {drInfo}, Welcome."

    session_attributes = getSessionAttributes(event)

    message2 = {
        'contentType': 'ImageResponseCard',
        'content': ' ',
        'imageResponseCard': {
            'title': 'Please select Option from below',
            'buttons': [
                {
                    'text': 'Show todays open appointments',
                    'value': 'Show todays open appointments'
                },
                {
                    'text': 'Exit',
                    'value': 'Exit'
                }

            ]
        }
    }

    return closeWithOptions(
        event,
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        },
        message2
    )


def appointment_handler(event):
    #session_attributes = init_or_load_session(event)

    slots = getSlots(event)
    name = getIntentName(event)
    print(name)
    dateValue = getSlot(event, 'dateValue')
    appointmentDetails = getAppointments(dateValue)
    json_appointmentDetails = appointmentDetails.to_json(orient='records')

    session_attributes = getSessionAttributes(event)

    return closeWithOptions(
        event,
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Please select one of the patient to proceed'
        },
        {
            'contentType': 'CustomPayload',
            'value': json_appointmentDetails
        }
    )

import logging
import json
import datetime
import dateutil.parser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def getDoctorInfo(phoneno):
    return "Dr. Hemant Viswas"

## TODO: Validate phone no


def getWelcomeSessionAttrib(event, phoneNo):

    # serialize new session data
    attribs = {
        'phoneNo': phoneNo
    }

    # fetch or initialize session
    session_attributes = event.get('sessionAttributes') or {}

    # update session data
    session_attributes['currentPhoneNo'] = json.dumps(attribs)

    return session_attributes

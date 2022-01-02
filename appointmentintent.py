import logging
import json
import datetime
import pandas as pd
import dateutil.parser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def getAppointments(dateValue):

    df = pd.DataFrame({
        'App Time': ['07:00 PM', '07:15 PM', '08:30 PM', '08:45 PM'],
        'Phone No': ['9002202200', '9002202201', '9002202202', '9002202203'],
        'Name': ['Anurag Singh', 'Mihir Ahuja', 'Rishabh Jain', 'Narrotam Das']
    })

    return df

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

import logging
import os
from typing import Optional

from twilio.rest import Client

from models import CallStatus


class CallProvider:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "0000000000000000000000000000000000")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "0000000000000000000000000000000000")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER", "+0000000000000000000000000000000000")
        self.twiml_bin_url = os.getenv("TWIML_BIN_URL",
                                       "https://handler.twilio.com/twiml/0000000000000000000000000000000000")

        if not all([self.account_sid, self.auth_token, self.phone_number, self.twiml_bin_url]):
            raise ValueError("Missing required Twilio credentials or TwiML Bin URL")

        self.client = Client(self.account_sid, self.auth_token)
        self.logger = logging.getLogger(__name__)

    def make_call(self, to_number: str, message: Optional[str] = None) -> dict:
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.phone_number,
                url=self.twiml_bin_url
            )
            self.logger.info(f"Call initiated to {to_number} with SID: {call.sid}")
            return {
                'success': True,
                'call_sid': call.sid,
                'status': CallStatus(call.status).value
            }
        except Exception as e:
            self.logger.error(f"Failed to initiate call: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_status(self, call_sid: str) -> CallStatus:
        try:
            call = self.client.calls(call_sid).fetch()
            return CallStatus(call.status)
        except Exception as e:
            self.logger.error(f"Failed to fetch call status: {str(e)}")
            raise

import logging
import os
from typing import Optional

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from models import CallStatus


class CallProvider:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "AC8a7cdb4007f0fa2d6478684de2507071")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "aa66038e12ef164ba05be1e31f045537")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER", "+17192495030")
        self.twiml_bin_url = os.getenv("TWIML_BIN_URL",
                                       "https://handler.twilio.com/twiml/EH4de5706bd7f1193d7bf7a737daccdd57")

        if not all([self.account_sid, self.auth_token, self.phone_number, self.twiml_bin_url]):
            raise ValueError("Missing required Twilio credentials or TwiML Bin URL")

        self.client = Client(self.account_sid, self.auth_token)
        self.logger = logging.getLogger(__name__)

    def generate_twiml(self, message: str) -> str:
        response = VoiceResponse()
        response.say(message)
        return str(response)

    def make_call(self, to_number: str, message: Optional[str] = None) -> dict:
        try:
            # Generate TwiML if message is provided, otherwise use the default TwiML bin URL
            twiml_param = {
                'twiml': self.generate_twiml(message) if message else None,
                'url': None if message else self.twiml_bin_url
            }

            call = self.client.calls.create(
                to=to_number,
                from_=self.phone_number,
                **{k: v for k, v in twiml_param.items() if v is not None}
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

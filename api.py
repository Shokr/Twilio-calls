import logging

from fastapi import FastAPI, HTTPException, status

from models import CallRequest
from providers import CallProvider

app = FastAPI()

provider = CallProvider()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.post("/calls", status_code=status.HTTP_201_CREATED)
async def create_call(call_request: CallRequest):
    """
    Initiates a voice call to the specified number with an optional message.

    Args:
        call_request (CallRequest): Request body containing the phone number and optional message.

    Returns:
        dict: Call initiation response with success status and call SID.
    """
    logger.info(f"Initiating call to {call_request.to_number}")
    result = provider.make_call(call_request.to_number, call_request.message)

    if not result.get('success'):
        logger.error(f"Call initiation failed: {result.get('error')}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get('error'))

    logger.info(f"Call initiated successfully with SID: {result.get('call_sid')}")
    return result


@app.get("/calls/{call_sid}", status_code=status.HTTP_200_OK)
async def get_call_status(call_sid: str):
    """
    Retrieves the status of a call using the call SID.

    Args:
        call_sid (str): Unique identifier for the call.

    Returns:
        dict: Call status response containing call SID and status.
    """
    logger.info(f"Fetching status for call SID: {call_sid}")

    try:
        status = provider.get_status(call_sid)
        return {"call_sid": call_sid, "status": status.value}
    except Exception as e:
        logger.error(f"Error fetching call status: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

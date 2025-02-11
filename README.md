# VOIP Call Service

This is a simple FastAPI service that allows users to initiate and track voice calls.

## Features

- Create a voice call
- Retrieve call status
- Logging for request tracking

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Shokr/Twilio-calls.git
   cd Twilio-calls
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the service:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### 1. Create a Call

- **Endpoint:** `POST /calls`
- **Request Body:**
  ```json
  {
    "to_number": "+1234567890",
    "message": "Hello, this is a test call."
  }
  ```
- **Response:**
  ```json
  {
  "success": true,
  "call_sid": "CAdf2d8ffbb6cd027b81b2eb27371ade4c",
  "status": "queued"
  }
  ```

### 2. Get Call Status

- **Endpoint:** `GET /calls/{call_sid}`
- **Response:**
  ```json
  {
  "call_sid": "CAdf2d8ffbb6cd027b81b2eb27371ade4c",
  "status": "completed"
  }
  ```

## Running Tests

To run unit tests:

```sh
pytest
```

## Docker Setup

1. Build the Docker image:
   ```sh
   docker build -t fastapi-call-service .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 fastapi-call-service
   ```


import uvicorn
from fastapi import FastAPI

from schemas import MessageInputModel
from api.api_grpc import grpc_client

app = FastAPI()


@app.post('/message')
def send_message(message_details: MessageInputModel):
    result = grpc_client.send_message(message_details.sender_name, message_details.text)
    return {'result': result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

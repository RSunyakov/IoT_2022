import grpc

from api_service_pb2_grpc import ApiServiceStub
from api_service_pb2 import MessageRequest


def send_message(sender_name, text):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ApiServiceStub(channel)
        stub_response = stub.SendMessage(MessageRequest(senderName=sender_name, text=text))
        return stub_response.result

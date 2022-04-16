import grpc
from concurrent import futures

from api.kafka.producer import Producer
from api_service_pb2 import MessageResponse
import api_service_pb2_grpc


class ApiService(api_service_pb2_grpc.ApiServiceServicer):
    def __init__(self):
        self.producer = Producer()
        super().__init__()

    def SendMessage(self, request, context):
        result = self.producer.produce(request.senderName, request.text)
        return MessageResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_service_pb2_grpc.add_ApiServiceServicer_to_server(ApiService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

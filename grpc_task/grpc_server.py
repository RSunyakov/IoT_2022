import grpc
import math
import numpy as np
from concurrent import futures

from math_service_pb2 import IntResponse, FloatResponse
import math_service_pb2_grpc


def factor(n):
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        ans.append(n)
    return ans


class MathService(math_service_pb2_grpc.MathServiceServicer):
    def Sqrt(self, request, context):
        return FloatResponse(numFloat=math.sqrt(request.numInt))

    def Std(self, request_iterator, context):
        nums = []
        for num in request_iterator:
            nums.append(num.numInt)
        return FloatResponse(numFloat=np.std(nums, axis=0))

    def Factor(self, request, context):
        for num in factor(request.numInt):
            yield IntResponse(numInt=num)

    def Max(self, request_iterator, context):
        local_max = None
        for num in request_iterator:
            if local_max is None:
                local_max = num.numInt
                yield IntResponse(numInt=local_max)
            elif local_max < num.numInt:
                local_max = num.numInt
                yield IntResponse(numInt=local_max)
            else:
                yield IntResponse(numInt=local_max)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    math_service_pb2_grpc.add_MathServiceServicer_to_server(MathService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

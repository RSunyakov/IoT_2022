import grpc
import math_service_pb2_grpc
from math_service_pb2 import IntRequest


def math_sqrt(stub, num):
    num_sqrt = stub.Sqrt(IntRequest(numInt=num))
    print(f'Sqrt of {num} = {num_sqrt.numFloat}')


def num_iterator(nums):
    for num in nums:
        yield IntRequest(numInt=num)


def math_std(stub, nums):
    it = num_iterator(nums)
    nums_std = stub.Std(it)
    print(f'Standard deviation of {nums} = {nums_std.numFloat}')


def math_factor(stub, num):
    nums = stub.Factor(IntRequest(numInt=num))
    print(f'Factors of {num} are')
    for item in nums:
        print(item.numInt)


def math_max(stub, nums):
    it = num_iterator(nums)
    maxes = stub.Max(it)
    print(f'Local max of {nums} is')
    for m in maxes:
        print(m.numInt)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = math_service_pb2_grpc.MathServiceStub(channel)
        print('----------Unary Call----------')
        math_sqrt(stub, 121)
        print('----------Client Streaming----------')
        math_std(stub, [1, 2, 3, 4, 5])
        print('----------Server Streaming----------')
        math_factor(stub, 1362)
        print('----------Bidirectional Streaming----------')
        math_max(stub, [5, 4, 6, 2, 1])


if __name__ == '__main__':
    run()

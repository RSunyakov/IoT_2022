from grpc_tools import protoc

protoc.main((
    '',
    '-I./proto',
    '--python_out=.',
    '--grpc_python_out=.',
    './proto/math_service.proto',
))

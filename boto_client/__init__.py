import boto3

def get_boto_client(service_name: str):
    boto3.set_stream_logger('botocore', level='INFO')
    session = boto3.Session(profile_name='default', region_name='us-east-1')
    client = session.client(service_name=service_name)
    return client
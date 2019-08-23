import uuid
import base64

def generate_id(prefix):
	return prefix + '-' + str(uuid.uuid4())

def base64_encode(data):
	return base64.b64encode(data)

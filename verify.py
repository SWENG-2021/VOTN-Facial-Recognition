"""
1. Extract the signature from the HTTP headers
2. Create a message to sign by combining the version, delivery time, and request body (v0:timestamp:body)
3. Compute the HMAC SHA256 signature using your signing secret.
4. Compare!
"""

import json, hmac, hashlib, math, time

def verifyWebhook(version, timestamp, payload, signature, secret):

	#stringify the payload
	body = json.dumps(payload, separators=(',', ':'))

	#timestamps - no older than 5 minutes
	currentTime = math.trunc(time.time())
	minutes = 5
	expired = (currentTime-timestamp) > minutes*60

	#generate signature
	msg = bytes('v0:'+str(timestamp)+':'+body, "ascii")
	hmac1 = hmac.new(bytes(secret, "ascii"), digestmod=hashlib.sha256)
	generateSignature = hmac1.update(msg)
	generateSignature = hmac1.hexdigest()

	#check if verified webhook
	return (not expired and signature == version+"="+generateSignature)



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



#TESTING ONLY--------------------------------------------------------------------------------
#sample secret key
sample_secret = 'yxSE59T0gtZOFZxw6UhLwTkhd2m8ntNSdSWnApQ0xOnMEzSoXbD8sGFP4bzb7MbS'

#sample data
sample_version = 'v0'
sample_signature = 'v0=a77ce6856e609c884575c2fd211d07a9ad1c3f72e19c06ff710e8f086ffca883'
sample_timestamp = 1604004499
sample_payload = {
	"project": {
		"id": "f348e9f4-f142-42f9-b3bf-478d93f0feb4"
	},
	"resource": {
		"id": "6aad9151-c216-4d6f-b5e9-530df551a426",
		"type": "asset"
	},
	"team": {
		"id": "aa891687-4b1e-4150-9b6d-9e4911c5b436"
	},
	"type": "asset.label.updated",
	"user": {
		"id": "59c9ade1-311b-4c3b-8231-b9d88e9a1a85"
	}
}

print(verifyWebhook(sample_version, sample_timestamp, sample_payload, sample_signature, sample_secret))
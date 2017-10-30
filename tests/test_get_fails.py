import requests
import uuid
import datetime


#get failures
get_fails = requests.get("http://127.0.0.1:5000/fail/{}".format("head"))
if get_fails.ok:
	print("Failures Returned:: {}".format(get_fails.json()))
else:
	print("Could Not get Full")
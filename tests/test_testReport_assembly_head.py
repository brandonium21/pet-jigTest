import requests
import uuid
import datetime

full_assembly_id = "966d4edb-56e4-4b20-8b92-279e415249d8"
fa_obj = None

# create test report "headass"
# assonent id / assonent type / testreport type / testreport id
# testreport object


# get full assembly
get_fa = requests.get("http://127.0.0.1:5000/fassemb/{}".format(full_assembly_id))
if get_fa.ok:
	fa_obj = get_fa.json()
	print("Full Assembly Returned:: {}".format(get_fa.json()))
else:
	print("Could Not get full Assembly")


# variables
ass_id = str(fa_obj['head'][0]['uid'])
ass_type = str(fa_obj['head'][0]['type'])
tr_type = "head"
tr_id = str(uuid.uuid4())
tr_obj = {
	'type': tr_type,
	'uid': tr_id,
	'file': "blah file name head assembly",
	'timestamp': str(datetime.datetime.utcnow()),
	'failed': True
}
r = "http://127.0.0.1:5000/treport/{}/{}/{}/{}".format(
	ass_id, ass_type, tr_type, tr_id
	)

# create test report
headass_testR = requests.post(r, json=tr_obj)
if headass_testR.ok:
	print("headass_testR Created:: {}".format(headass_testR.json()))
	tr_id = tr_id
else:
	tr_id = None

#get updated test report
get_headass = requests.get("http://127.0.0.1:5000/hassemb/{}".format(ass_id))
if get_headass.ok:
	print("headass  Returned:: {}".format(get_headass.json()))
else:
	print("Could Not get headass")
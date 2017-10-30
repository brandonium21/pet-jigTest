import requests
import uuid
import datetime

full_assembly_id = "966d4edb-56e4-4b20-8b92-279e415249d8"
fa_obj = None

# create test report "FUll Assembly"
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
ass_id = str(fa_obj['uid'])
ass_type = str(fa_obj['type'])
tr_type = "full"
tr_id = str(uuid.uuid4())
tr_obj = {
	'type': tr_type,
	'uid': tr_id,
	'file': "blah file name head full",
	'timestamp': str(datetime.datetime.utcnow()),
	'failed': True
}
r = "http://127.0.0.1:5000/treport/{}/{}/{}/{}".format(
	ass_id, ass_type, tr_type, tr_id
	)

# create test report
full_testR = requests.post(r, json=tr_obj)
if full_testR.ok:
	print("full_testR Created:: {}".format(full_testR.json()))
	tr_id = tr_id
else:
	tr_id = None

#get updated test report
get_full = requests.get("http://127.0.0.1:5000/fassemb/{}".format(ass_id))
if get_full.ok:
	print("Full  Returned:: {}".format(get_full.json()))
else:
	print("Could Not get Full")
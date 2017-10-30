import requests
import uuid
import datetime

full_assembly_id = "966d4edb-56e4-4b20-8b92-279e415249d8"
fa_obj = None

# create test report "mrf"
# component id / component type / testreport type / testreport id
# testreport object


# get full assembly
get_fa = requests.get("http://127.0.0.1:5000/fassemb/{}".format(full_assembly_id))
if get_fa.ok:
	fa_obj = get_fa.json()
	print("Full Assembly Returned:: {}".format(get_fa.json()))
else:
	print("Could Not get full Assembly")


# variables
comp_id = str(fa_obj['rear'][0]['components'][0]['uid'])
comp_type = str(fa_obj['rear'][0]['components'][0]['type'])
tr_type = "rcomp"
tr_id = str(uuid.uuid4())
tr_obj = {
	'type': tr_type,
	'uid': tr_id,
	'file': "blah file name mrf",
	'timestamp': str(datetime.datetime.utcnow()),
	'failed': True
}
r = "http://127.0.0.1:5000/treport/{}/{}/{}/{}".format(
	comp_id, comp_type, tr_type, tr_id
	)

# create test report
mrf_testR = requests.post(r, json=tr_obj)
if mrf_testR.ok:
	print("mrf_testR Created:: {}".format(mrf_testR.json()))
	tr_id = tr_id
else:
	tr_id = None

#get updated test report
get_mrf = requests.get("http://127.0.0.1:5000/component/{}/{}".format(comp_id, "mrf"))
if get_mrf.ok:
	print("mrf Component Returned:: {}".format(get_mrf.json()))
else:
	print("Could Not get mrf Component")
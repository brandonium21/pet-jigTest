import requests
import uuid
import datetime

full_assembly_id = "966d4edb-56e4-4b20-8b92-279e415249d8"
fa_obj = None

# create test report "mff"
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
comp_id = str(fa_obj['head'][0]['components'][0]['uid'])
comp_type = str(fa_obj['head'][0]['components'][0]['type'])
tr_type = "hcomp"
tr_id = str(uuid.uuid4())
tr_obj = {
	'type': tr_type,
	'uid': tr_id,
	'file': "blah file name mff",
	'timestamp': str(datetime.datetime.utcnow()),
	'failed': True
}
r = "http://127.0.0.1:5000/treport/{}/{}/{}/{}".format(
	comp_id, comp_type, tr_type, tr_id
	)

# create test report
mff_testR = requests.post(r, json=tr_obj)
if mff_testR.ok:
	print("mff_testR Created:: {}".format(mff_testR.json()))
	tr_id = tr_id
else:
	tr_id = None

#get updated test report
get_mff = requests.get("http://127.0.0.1:5000/component/{}/{}".format(comp_id, "mff"))
if get_mff.ok:
	print("mff Component Returned:: {}".format(get_mff.json()))
else:
	print("Could Not get mff Component")
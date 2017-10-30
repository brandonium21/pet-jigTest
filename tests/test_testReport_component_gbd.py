import requests
import uuid
import datetime

full_assembly_id = "966d4edb-56e4-4b20-8b92-279e415249d8"
fa_obj = None

# create test report "gbd"
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
	'file': "blah file name gbd",
	'timestamp': str(datetime.datetime.utcnow()),
	'failed': True
}
r = "http://127.0.0.1:5000/treport/{}/{}/{}/{}".format(
	comp_id, comp_type, tr_type, tr_id
	)

# create test report
gbd_testR = requests.post(r, json=tr_obj)
if gbd_testR.ok:
	print("gbd_testR Created:: {}".format(gbd_testR.json()))
	tr_id = tr_id
else:
	tr_id = None

#get updated test report
get_gbd = requests.get("http://127.0.0.1:5000/component/{}/{}".format(comp_id, "gbd"))
if get_gbd.ok:
	print("gbd Component Returned:: {}".format(get_gbd.json()))
else:
	print("Could Not get gbd Component")
import requests
import uuid
# create head component "mff"
mff_id = str(uuid.uuid4())
mff = requests.post("http://127.0.0.1:5000/component/mff/{}".format(mff_id))
if mff.ok:
	print("MFF Created:: {}".format(mff.json()))
	mff_id = mff_id
else:
	mff_id = None

# create rear comonents "mrf", "te", "gbd", "gbt"
mrf_id = str(uuid.uuid4())
mrf = requests.post("http://127.0.0.1:5000/component/mrf/{}".format(mrf_id))
if mrf.ok:
	print("MRF Created:: {}".format(mrf.json()))
	mrf_id = mrf_id
else:
	mrf_id = None

te_id = str(uuid.uuid4())
te = requests.post("http://127.0.0.1:5000/component/te/{}".format(te_id))
if te.ok:
	print("TE Created:: {}".format(te.json()))
	te_id = te_id
else:
	te_id = None

gbd_id = str(uuid.uuid4())
gbd = requests.post("http://127.0.0.1:5000/component/gbd/{}".format(gbd_id))
if gbd.ok:
	print("GBD Created:: {}".format(gbd.json()))
	gbd_id = gbd_id
else:
	gbd_id = None

gbt_id = str(uuid.uuid4())
gbt = requests.post("http://127.0.0.1:5000/component/gbt/{}".format(gbt_id))
if gbt.ok:
	print("GBT Created:: {}".format(gbt.json()))
	gbt_id = gbt_id
else:
	gbt_id = None

# create head assembly
ha_id = str(uuid.uuid4())
ha = requests.post("http://127.0.0.1:5000/hassemb/{}/{}/{}".format(mff_id, ha_id, "headass"))
if ha.ok:
	print("Head Assembly Created:: {}".format(ha.json()))
	ha_id = ha_id
else:
	ha_id = None

print mrf_id
print te_id
print gbd_id
print gbt_id

# create rear assembly
ra_id = str(uuid.uuid4())
ra = requests.post("http://127.0.0.1:5000/rassemb/{}/{}/{}/{}/{}/{}".format(mrf_id, te_id, gbd_id, gbt_id, ra_id, "rearass"))
if ra.ok:
	print("Rear Assembly Created:: {}".format(ra.json()))
	ra_id = ra_id
else:
	ra_id = None


# create full assembly
fa_id = str(uuid.uuid4())
fa = requests.post("http://127.0.0.1:5000/fassemb/{}/{}/{}/{}".format(ha_id, ra_id, "fullass", fa_id))
if fa.ok:
	print("Full Assembly Created:: {}".format(fa.json()))
	fa_id = fa_id
else:
	fa_id = None

print fa_id

# get full assembly
get_fa = requests.get("http://127.0.0.1:5000/fassemb/{}".format(fa_id))
if get_fa.ok:
	print("Full Assembly Returned:: {}".format(get_fa.json()))
else:
	print("Could Not get full Assembly")

'''
# get rear assembly
get_ra = requests.get("http://127.0.0.1:5000/rassemb/{}".format(ra_id))
if get_ra.ok:
	print("Rear Assembly Returned:: {}".format(get_ra.json()))
else:
	print("Could Not get rear Assembly")
'''
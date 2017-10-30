from models import *


def check_test(t_type, t_id):
    if t_type == 'rear':
        new_tr = TestReportRear(t_type, t_id)
        db.session.add(new_tr)
        db.session.commit()
        return TestReportRear.query.filter_by(uid=t_id).first()
    if t_type == 'head':
        new_tr = TestReportHead(t_type, t_id)
        db.session.add(new_tr)
        db.session.commit()
        return TestReportHead.query.filter_by(uid=t_id).first()
    if t_type == 'full':
        new_tr = TestReportFull(t_type, t_id)
        db.session.add(new_tr)
        db.session.commit()
        return TestReportFull.query.filter_by(uid=t_id).first()
    if t_type == 'rcomp':
        new_tr = TestReportComponentRear(t_type, t_id)
        db.session.add(new_tr)
        db.session.commit()
        return TestReportComponentRear.query.filter_by(uid=t_id).first()
    if t_type == 'hcomp':
        new_tr = TestReportComponentHead(t_type, t_id)
        db.session.add(new_tr)
        db.session.commit()
        return TestReportComponentHead.query.filter_by(uid=t_id).first()
    else:
        return False

def check_component(c_id, c_type):
    if c_type == 'rear' or c_type == 'rearass':
        return RearAssembly.query.filter_by(uid=c_id).first()
    if c_type == 'head' or c_type == 'headass':
        return HeadAssembly.query.filter_by(uid=c_id).first()
    if c_type == 'full' or c_type == 'fullass':
        return FullAssembly.query.filter_by(uid=c_id).first()
    if c_type in rear_types:
        return RearComponent.query.filter_by(uid=c_id).first()
    if c_type in head_types:
        return HeadComponent.query.filter_by(uid=c_id).first()
    else:
        return False

def check_component_all(c_type):
    if c_type == 'rear':
        return TestReportRear.query.filter_by(failed=True).all()
    if c_type == 'head':
        return TestReportHead.query.filter(TestReportHead.failed==True).first()
    if c_type == 'full':
        return TestReportFull.query.filter_by(failed=True).all()
    if c_type in rear_types:
        return TestReportComponentRear.query.filter_by(failed=True).all()
    if c_type in head_types:
        return TestReportComponentHead.query.filter_by(failed=True).all()
    else:
        return False

def check_get_tr(t_id, t_type):
    if t_type == 'rear':
        return TestReportRear.query.filter_by(uid=t_id).first()
    if t_type == 'head':
        return TestReportHead.query.filter_by(uid=t_id).first()
    if t_type == 'full':
        return TestReportFull.query.filter_by(uid=t_id).first()
    if t_type == 'rcomp':
        return TestReportComponentRear.query.filter_by(uid=t_id).first()
    if t_type == 'hcomp':
        return TestReportComponentHead.query.filter_by(uid=t_id).first()
    else:
        return False


# Marshmallow mappings
# *schema.dump(obj).data
full_assembly = FullAssemblySchema()
head_assembly = HeadAssemblySchema()
rear_assembly = RearAssemblySchema()
rear_component = RearComponentSchema()
head_component = HeadComponentSchema()
rear_component_tr = TestReportComponentRearSchema()
head_component_tr = TestReportComponentHeadSchema()
rear_tr = TestReportRearSchema()
full_tr = TestReportFullSchema()
head_tr = TestReportHeadSchema()

comp_map = {
    "rear": rear_component,
    "head": head_component,
    "mff": head_component,
    "mrf": rear_component,
    "te": rear_component,
    "gbd": rear_component,
    "gbt": rear_component
}

tr_map = {
    "rcomp": rear_component_tr,
    "hcomp": head_component_tr,
    "rear": rear_tr,
    "full": full_tr,
    "head": head_tr
}

# Type list
rear_types = ["mrf", "te", "gbd", "gbt"]
head_types = ["mff"]

#update status of all parents if foreign key updated
#the primary key changes uid stays the same
#make broker that gets data and send to database

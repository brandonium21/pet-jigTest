from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from models import *
from app_db_api import api, app, db, manager
from util import *
import json
import datetime


base_parser = reqparse.RequestParser()

# Add To db Resources
class ComponentR(Resource):
    def post(self, c_type, c_id):
        check = None
        if c_type in rear_types:
            print "REAR TYPE"
            new_comp = RearComponent(c_type, c_id)
        elif c_type in head_types:
            print "HEAD TYPE"
            new_comp = HeadComponent(c_type, c_id)
        else:
            return "Could Not find type", 400

        # add to db
        db.session.add(new_comp)
        db.session.commit()

        # query save data
        if c_type in rear_types:
            check = RearComponent.query.filter_by(uid=c_id).first()
        if c_type in head_types:
            check = HeadComponent.query.filter_by(uid=c_id).first()

        if check:
            return comp_map[c_type].dump(check).data, 201
        return "Could Not upload", 400

    def get(self, comp_id, comp_type):
        if comp_type in rear_types:
            comp = RearComponent.query.filter_by(uid=comp_id).first()
        if comp_type in head_types:
            comp = HeadComponent.query.filter_by(uid=comp_id).first()

        if comp:
            return comp_map[comp_type].dump(comp).data, 201
        return "Could Not Find Component", 400

class RearAssemblyR(Resource):
    def post(self, mrf_id, te_id, gbd_id, gbt_id, ra_id, type):
        mrf_comp = RearComponent.query.filter_by(uid=mrf_id).first()
        te_comp = RearComponent.query.filter_by(uid=te_id).first()
        gbd_comp = RearComponent.query.filter_by(uid=gbd_id).first()
        gbt_comp = RearComponent.query.filter_by(uid=gbt_id).first()

        if mrf_comp and te_comp and gbd_comp and gbt_comp:
            # create rear assembly and commit to db
            new_ra = RearAssembly(type, ra_id)
            db.session.add(new_ra)
            db.session.commit()

            # get ra db obj
            ra = RearAssembly.query.filter_by(uid=ra_id).first()
            mrf_comp.assembly = ra.id
            te_comp.assembly = ra.id
            gbd_comp.assembly = ra.id
            gbt_comp.assembly = ra.id
            db.session.commit()

            return rear_assembly.dump(ra).data
        return "Could not find all Components needed", 400

    def get(self, ra_id):
        rear = RearAssembly.query.filter_by(uid=ra_id).first()
        if rear:
            return rear_assembly.dump(rear).data, 201
        return "Could Not Find RearAssembly", 400

class HeadAssemblyR(Resource):
    def post(self, mff_id, ha_id, type):
        mff_comp = HeadComponent.query.filter_by(uid=mff_id).first()

        # create head assembly and commit to db
        new_ha = HeadAssembly(type, ha_id)
        db.session.add(new_ha)
        db.session.commit()

        # get ha db obj
        ha = HeadAssembly.query.filter_by(uid=ha_id).first()
        mff_comp.assembly = ha.id
        db.session.commit()

        return head_assembly.dump(ha).data

    def get(self, ha_id):
        head = HeadAssembly.query.filter_by(uid=ha_id).first()
        if head:
            return head_assembly.dump(head).data, 201
        return "Could Not Find HeadAssembly", 400

class FullAssemblyR(Resource):
    def post(self, head_id, rear_id, type, fa_id):
        # query head and rear
        head = HeadAssembly.query.filter_by(uid=head_id).first()
        rear = RearAssembly.query.filter_by(uid=rear_id).first()
        if head and rear:
            # create full assembly and commit to db
            new_fa = FullAssembly(type, fa_id)
            db.session.add(new_fa)
            db.session.commit()

            # connect rear and head to full assembly
            
            fa = FullAssembly.query.filter_by(uid=fa_id).first()
            head.assembly = fa.id
            rear.assembly = fa.id
            db.session.commit()

            # get updated data
            up_fa = FullAssembly.query.filter_by(uid=fa_id).first()
            return full_assembly.dump(up_fa).data, 201
        return "Could not find head or rear", 400

    def get(self, fa_id):
        full = FullAssembly.query.filter_by(uid=fa_id).first()
        #.join(FullAssembly.head_component)
        if full:
            return full_assembly.dump(full).data, 201
        return "Could Not Find FullAssembly", 400

class TestReportR(Resource):
    def post(self, c_id, c_type, tr_type, tr_id):
        # Define data parser schema
        parser = base_parser.copy()
        parser.add_argument('type', type=str)
        parser.add_argument('uid', type=str)
        parser.add_argument('file', type=str)
        parser.add_argument('timestamp', type=str)
        parser.add_argument('failed', type=bool)
        print "hi"
        comp = check_component(c_id, c_type)
        if comp:
            print "hello"
            # Create Test Report
            tr = check_test(tr_type, tr_id)
            if tr:
                args = parser.parse_args()
                print args['file']
                tr.file = args['file']
                tr.timestamp = datetime.datetime.strptime(args['timestamp'] , "%Y-%m-%d %H:%M:%S.%f")
                tr.failed = args['failed']
                tr.component = comp.id
                db.session.commit()
            else:
                return "FAILED: wrong type of report", 400

        else:
            return "FAILED: No component", 400
        return tr_map[tr_type].dump(tr).data, 201

    def get(self, tr_id, tr_type):
        tr = check_get_tr(tr_id, tr_type)
        if tr:
            return tr_map[tr_type].dump(tr).data, 201
        else:
            return "FAILED: No Test Report", 400

# Active Resources
class Failures(Resource):
    def get(self, c_type): # get all failure for given level type
        failed_comps = check_component_all(c_type)
        if failed_comps:
            return comp_map[c_type].dump(failed_comps).data, 201
        return "No Failed Components", 400
    def post(self, c_type, c_id): # get all failures for a given component
        return



## Api resource routing
                            #       GET                         POST
api.add_resource(ComponentR, '/component/<string:comp_id>/<string:comp_type>', '/component/<string:c_type>/<string:c_id>')
api.add_resource(RearAssemblyR, '/rassemb/<string:ra_id>', '/rassemb/<string:mrf_id>/<string:te_id>/<string:gbd_id>/<string:gbt_id>/<string:ra_id>/<string:type>')
api.add_resource(HeadAssemblyR, '/hassemb/<string:ha_id>', '/hassemb/<string:mff_id>/<string:ha_id>/<string:type>')
api.add_resource(FullAssemblyR, '/fassemb/<string:fa_id>', '/fassemb/<string:head_id>/<string:rear_id>/<string:type>/<string:fa_id>')
api.add_resource(TestReportR, '/treport/<string:tr_id>/<string:tr_type>', '/treport/<string:c_id>/<string:c_type>/<string:tr_type>/<string:tr_id>')
api.add_resource(Failures, '/fail/<string:c_type>', '/fail/<string:c_type>/<string:c_id>')

## restless endpoints
# Create API endpoints, which will be available at /api/<tablename>
manager.create_api(FullAssembly, methods=['GET'])

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)
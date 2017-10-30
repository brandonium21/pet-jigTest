from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app_db_api import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, post_dump


class TestReportFull(db.Model):
    __tablename__ = 'tr_full'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    uid = db.Column(db.String(600), unique=True)
    file = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime(), unique=True)
    failed = db.Column(db.Boolean())
    component = db.Column(db.Integer, db.ForeignKey('full_assembly.id'))

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<TestReportFull: type=%r, uid=%r, file=%r>' % self.type, self.uid, self.file

class TestReportFullSchema(ModelSchema):
    class Meta:
        model = TestReportFull

class TestReportRear(db.Model):
    __tablename__ = 'tr_rear'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    status = db.Column(db.String(20))
    uid = db.Column(db.String(600), unique=True)
    file = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime(), unique=True)
    failed = db.Column(db.Boolean())
    component = db.Column(db.Integer, db.ForeignKey('rear_assembly.id'))

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<TestReportRear: type=%r, uid=%r, file=%r>' % self.type, self.uid, self.file

class TestReportRearSchema(ModelSchema):
    class Meta:
        model = TestReportRear


class TestReportComponentRear(db.Model):
    __tablename__ = 'rear_component_tr'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    uid = db.Column(db.String(600), unique=True)
    file = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime, unique=True)
    failed = db.Column(db.Boolean)
    component = db.Column(db.Integer, db.ForeignKey('rear_component.id'))

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<TestReportComponent: type=%r, uid=%r, file=%r>' % self.type, self.uid, self.file

class TestReportComponentRearSchema(ModelSchema):
    class Meta:
        model = TestReportComponentRear


class RearComponent(db.Model):
    __tablename__ = 'rear_component'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    status = db.Column(db.String(20))
    uid = db.Column(db.String(600), unique=True)
    assembly = db.Column(db.Integer, db.ForeignKey('rear_assembly.id'))
    test_reports = db.relationship('TestReportComponentRear',
        backref='rear_component', lazy=True)

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<Component: type=%r, uid=%r>' % self.type, self.uid

class RearComponentSchema(ModelSchema):
    test_reports = fields.Nested(TestReportComponentRearSchema, many=True)
    class Meta:
        model = RearComponent

class RearAssembly(db.Model):
    __tablename__ = 'rear_assembly'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), unique=True)
    status = db.Column(db.String(20))
    uid = db.Column(db.String(600))
    assembly = db.Column(db.Integer, db.ForeignKey('full_assembly.id'))
    components = db.relationship('RearComponent',
        backref='rear_assembly', lazy=True)
    test_reports = db.relationship('TestReportRear',
        backref='rear_assembly', lazy=True)

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<RearAssembly: type=%r, uid=%r>' % self.type, self.uid

class RearAssemblySchema(ModelSchema):
    components = fields.Nested(RearComponentSchema, many=True)
    test_reports = fields.Nested(TestReportRearSchema, many=True)
    class Meta:
        model = RearAssembly

class TestReportComponentHead(db.Model):
    __tablename__ = 'tr_comp_head'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    uid = db.Column(db.String(600), unique=True)
    file = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime, unique=True)
    failed = db.Column(db.Boolean)
    component = db.Column(db.Integer, db.ForeignKey('head_component.id'))

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<TestReportComponent: type=%r, uid=%r, file=%r>' % self.type, self.uid, self.file

class TestReportComponentHeadSchema(ModelSchema):
    class Meta:
        model = TestReportComponentHead


class HeadComponent(db.Model):
    __tablename__ = 'head_component'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    status = db.Column(db.String(20))
    uid = db.Column(db.String(600), unique=True)
    curr_tr = db.Column(db.Integer, db.ForeignKey('head_component.id'))
    assembly = db.Column(db.Integer, db.ForeignKey('head_assembly.id'))
    test_reports = db.relationship('TestReportComponentHead',
        backref='head_component', lazy=True)

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<Component: type=%r, uid=%r>' % self.type, self.uid

class HeadComponentSchema(ModelSchema):
    test_reports = fields.Nested(TestReportComponentHeadSchema, many=True)
    class Meta:
        model = HeadComponent

class TestReportHead(db.Model):
    __tablename__ = 'tr_head'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    uid = db.Column(db.String(600), unique=True)
    file = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime(), unique=True)
    failed = db.Column(db.Boolean())
    component = db.Column(db.Integer, db.ForeignKey('head_assembly.id'))

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<TestReportHead: type=%r, uid=%r, file=%r>' % self.type, self.uid, self.file

class TestReportHeadSchema(ModelSchema):
    class Meta:
        model = TestReportHead


class HeadAssembly(db.Model):
    __tablename__ = 'head_assembly'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    type = db.Column(db.String(80), unique=True)
    uid = db.Column(db.String(600))
    assembly = db.Column(db.Integer, db.ForeignKey('full_assembly.id'))
    components = db.relationship('HeadComponent',
        backref='head_assembly', lazy=True)
    test_reports = db.relationship('TestReportHead',
        backref='head_assembly', lazy=True)

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<HeadAssembly: type=%r, uid=%r>' % self.type, self.uid

class HeadAssemblySchema(ModelSchema):
    components = fields.Nested(HeadComponentSchema, many=True)
    test_reports = fields.Nested(TestReportHeadSchema, many=True)
    class Meta:
        model = HeadAssembly



class FullAssembly(db.Model):
    __tablename__ = 'full_assembly'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), unique=True)
    uid = db.Column(db.String(600))
    status = db.Column(db.String(20))
    test_reports = db.relationship('TestReportFull',
        backref='full_assembly', lazy=True)
    rear = db.relationship('RearAssembly',
        backref='full_assembly', lazy=True)
    head = db.relationship('HeadAssembly',
        backref='full_assembly', lazy=True) 

    def __init__(self, type, uid):
        self.type = type
        self.uid = uid

    def __repr__(self):
        return '<FullAssembly: type=%r, uid=%r, rear=%r, head=%r>' % self.type, self.uid, self.rear_component, self.head_component

class FullAssemblySchema(ModelSchema):
    test_reports = fields.Nested(TestReportFullSchema, many=True)
    rear = fields.Nested(RearAssemblySchema, many=True)
    head = fields.Nested(HeadAssemblySchema, many=True)
    class Meta:
        model = FullAssembly

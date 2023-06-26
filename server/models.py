from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Research(db.Model,SerializerMixin):
    __tablename__ = 'researches'
    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)

    # add relationships and rules and validations
    research_authors = db.relationship("ResearchAuthors", backref='research_paper')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    serialize_rules = ('-research_Auhtors.research_paper', '-created_at', '-updated_at')

    @validates('year')
    def validate_year(self, key, value):
        if not len(str(value)) == 4:
            raise ValueError('enter valid year pls')
        return value

class Author(db.Model,SerializerMixin):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # add relationships and rules and validations
    research_authors = db.relationship("ResearchAuthors", backref='authors')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    serialize_rules = ('-research_Authors.authors', '-created_at', '-updated_at')

    @validates('field_of_study')
    def validate_field_of_study(self, key, value):
        valid_fos = ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']
        if value not in valid_fos:
            raise ValueError('enter valid field of study pls')
        return value


class ResearchAuthors(db.Model,SerializerMixin):
    __tablename__ = "research_Authors"
    id = db.Column(db.Integer, primary_key = True)

    # add relationships and rules and validations
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    serialize_rules = ('-authors.research_Authors', '-research_paper.research_Authors', '-created_at', '-updated_at')

    
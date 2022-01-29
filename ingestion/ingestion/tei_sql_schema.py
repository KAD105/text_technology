"""
This module contains class definitions for the tables storing objects transformed from
    TEI format xml corpora.

    In all honesty, this is a toy project so this probably wont describe  anything
    except https://dracor.org/api/corpora/shake/play/two-gentlemen-of-verona/tei
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy as sa

Base = declarative_base()

cast_stage_association_table = sa.Table(
    'cast_stage_association',
    Base.metadata,
    sa.Column('cast_item_id', sa.ForeignKey('cast_item.id'), primary_key=True),
    sa.Column('stage_id', sa.ForeignKey('stage.id'), primary_key=True)
)


# meta information
# TODO: meta information in TeiHeader missing

# cast information
class CastItem(Base):
    __tablename__ = "cast_item"

    id = sa.Column(sa.String(36), primary_key=True)
    # TODO: most of the current relationships are one to many
    #  -> figure out where bidrectional relationships are necessary
    cast_group_id = sa.Column(sa.ForeignKey("cast_group.id"))
    name = sa.Column(sa.TEXT)
    content = sa.Column(sa.TEXT)
    # TODO: corresp. attrib missing
    stages = relationship(
        "Stage",
        secondary=cast_stage_association_table,
        backref="stage"
    )


class CastRole(Base):
    __tablename__ = "cast_role"

    id = sa.Column(sa.String(36), primary_key=True)
    cast_item_id = sa.Column(sa.ForeignKey("cast_item.id"))
    name = sa.Column(sa.TEXT)
    content = sa.Column(sa.TEXT)
    description = sa.Column(sa.TEXT)


class CastGroup(Base):
    __tablename__ = "cast_group"

    id = sa.Column(sa.String(36), primary_key=True)


# play information
class Act(Base):
    __tablename__ = "act"

    id = sa.Column(sa.String(36), primary_key=True)
    content = sa.Column(sa.TEXT)


class Scene(Base):
    __tablename__ = "scene"

    id = sa.Column(sa.String(36), primary_key=True)
    act_id = sa.Column(sa.ForeignKey("act.id"))
    content = sa.Column(sa.TEXT)


class Stage(Base):
    __tablename__ = "stage"

    id = sa.Column(sa.String(36), primary_key=True)
    scene_id = sa.Column(sa.ForeignKey("scene.id"), index=True)
    content = sa.Column(sa.TEXT)
    cast = relationship(
        "CastItem",
        secondary=cast_stage_association_table,
        backref="cast_item"
    )


class Speech(Base):
    __tablename__ = "speech"

    id = sa.Column(sa.String(36), primary_key=True)
    scene_id = sa.Column(sa.ForeignKey("scene.id"))
    cast_item_id = sa.Column(sa.ForeignKey("cast_item.id"))


class Line(Base):
    __tablename__ = "line"

    id = sa.Column(sa.String(36), primary_key=True)
    speech_id = sa.Column(sa.ForeignKey("speech.id"))


class Token(Base):
    __tablename__ = "token"

    id = sa.Column(sa.String(36), primary_key=True)
    line_id = sa.Column(sa.ForeignKey("line.id"))
    content = sa.Column(sa.TEXT)
    lemma = sa.Column(sa.TEXT)
    ana = sa.Column(sa.TEXT)

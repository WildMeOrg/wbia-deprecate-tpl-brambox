#
#   Copyright EAVISE
#

from enum import Enum

from .. import box as b
from ..annotations import annotation as anno

__all__ = ['Detection', 'ParserType', 'Parser']


class Detection(b.Box):
    """ Generic detection representation """
    def __init__(self):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """
        super(Detection, self).__init__()
        self.confidence = 0.0       # Confidence score in percentage

    @classmethod
    def create(cls, obj=None):
        """ Create a detection from a string or other box object """
        instance = super(Detection, cls).create(obj)

        if obj is None:
            return instance

        if isinstance(obj, Detection):
            instance.confidence = obj.confidence
        elif isinstance(obj, anno.Annotation):
            instance.confidence = 100.0

        return instance

    def __str__(self):
        """ pretty print """
        string = "Detection { "
        string += "\tclass_label = {}, ".format(self.class_label)
        string += "\tobject_id = {}, ".format(self.object_id)
        string += "\tx_top_left = {}, ".format(self.x_top_left)
        string += "\ty_top_left = {}, ".format(self.y_top_left)
        string += "\twidth = {}, ".format(self.width)
        string += "\theight = {}, ".format(self.height)
        string += "\tconfidence = {}".format(self.confidence)
        string += "}"

        return string

ParserType = b.ParserType

class Parser(b.Parser):
    """ Generic parser class """
    box_type = Detection        # Derived classes should set the correct box_type
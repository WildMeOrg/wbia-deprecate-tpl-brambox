#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
"""
Pascal VOC
----------
This parser can parse detections in the `pascal voc`_ format.
This format consists of one file per class of detection. |br|
confidence_scores are saved as a number between 0-1, coordinates are saved as pixel values.

Args:
    class_label (string): This keyword argument contains the ``class_label`` for the current file that is being parsed.

Example:
    >>> person.txt
        <img_000> <confidence_score> <x_left> <y_upper> <x_right> <y_lower>
        <img_000> <confidence_score> <x_left> <y_upper> <x_right> <y_lower>
        <img_073> <confidence_score> <x_left> <y_upper> <x_right> <y_lower>
    >>> cat.txt
        <img_011> <confidence_score> <x_left> <y_upper> <x_right> <y_lower>
"""

from .detection import *

__all__ = ["PascalVOCDetection", "PascalVOCParser"]


class PascalVOCDetection(Detection):
    """ Pascal VOC image detection """

    def serialize(self):
        """ generate a Pascal VOC detection string """
        raise NotImplementedError

    def deserialize(self, det_string, class_label):
        """ parse a Pascal VOC detection string """
        self.class_label = class_label

        elements = det_string.split()
        self.confidence = float(elements[1])
        self.x_top_left = float(elements[2])
        self.y_top_left = float(elements[3])
        self.width = float(elements[4]) - self.x_top_left
        self.height = float(elements[5]) - self.y_top_left

        self.object_id = 0

        return elements[0]


class PascalVOCParser(Parser):
    """ Pascal VOC detection parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = PascalVOCDetection
    extension = '.txt'

    def __init__(self, **kwargs):
        try:
            self.class_label = kwargs['class_label']
        except KeyError:
            self.class_label = ''

    def serialize(self, detections):
        """ Serialize input dictionary of detections into one string """
        raise NotImplementedError

    def deserialize(self, string):
        """ Deserialize a detection file into a dictionary of detections """
        result = {}

        for line in string.splitlines():
            if line[0] != '#':
                anno = self.box_type()
                img_id = anno.deserialize(line, self.class_label)
                if img_id in result:
                    result[img_id].append(anno)
                else:
                    result[img_id] = [anno]

        return result

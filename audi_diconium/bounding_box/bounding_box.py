import json
import numpy as np
import logging


class BoundingBox:
    def __init__(self, path):
        self.logger = logging.getLogger(BoundingBox.__name__)
        self.logger.info("Bounding Box is Intialized")
        self.path = path


    def skew_sym_matrix(self, u):
        return np.array([[0, -u[2], u[1]],
                         [u[2], 0, -u[0]],
                         [-u[1], u[0], 0]])

    def axis_angle_to_rotation_mat(self, axis, angle):
        return np.cos(angle) * np.eye(3) + np.sin(angle) * self.skew_sym_matrix(axis) + (1 - np.cos(angle)) * np.outer(
            axis, axis)

    def read_bounding_boxes(self, file_name_bboxes):
        # open the file
        with open(file_name_bboxes, 'r') as f:
            bboxes = json.load(f)

        boxes = []  # a list for containing bounding boxes
        self.logger.info("Bounding Box keys: {}". format(bboxes.keys()))

        for bbox in bboxes.keys():
            bbox_read = {}  # a dictionary for a given bounding box
            bbox_read['class'] = bboxes[bbox]['class']
            bbox_read['truncation'] = bboxes[bbox]['truncation']
            bbox_read['occlusion'] = bboxes[bbox]['occlusion']
            bbox_read['alpha'] = bboxes[bbox]['alpha']
            bbox_read['top'] = bboxes[bbox]['2d_bbox'][0]
            bbox_read['left'] = bboxes[bbox]['2d_bbox'][1]
            bbox_read['bottom'] = bboxes[bbox]['2d_bbox'][2]
            bbox_read['right'] = bboxes[bbox]['2d_bbox'][3]
            bbox_read['center'] = np.array(bboxes[bbox]['center'])
            bbox_read['size'] = np.array(bboxes[bbox]['size'])
            angle = bboxes[bbox]['rot_angle']
            axis = np.array(bboxes[bbox]['axis'])
            bbox_read['rotation'] = self.axis_angle_to_rotation_mat(axis, angle)
            boxes.append(bbox_read)

        return boxes

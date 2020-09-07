import os
import inspect
import logging
from glob import iglob
import cv2
from audi_diconium.bounding_box.bounding_box import *


class AudiConfigParser():
    def __init__(self, path):

        self.logger = logging.getLogger(AudiConfigParser.__name__)
        self.logger.info("Parser Intialized")

        if os.path.exists(path):
            self._dirname = path
            self._bounding_path = self._dirname.replace('cams_lidars.json', 'camera_lidar_semantic_bboxes')
            print("Bounding path", self._bounding_path)
            self.logger.info("Bounding Path: {}".format(self._bounding_path))
            try:
                with open(self._dirname, 'r') as f:
                    self._config = json.load(f)
            except FileNotFoundError:
                self.logger.info("File does not exist in path: {}".format(self._dirname))
        else:
            self.get_directory()

    def get_directory(self):

        self._dirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).replace("core",
                                                                                                          "data")
        self._dirname = os.path.join(self._dirname, "a2d2", "cams_lidars.json")
        print("self.dirname", self._dirname)
        self.logger.info("Directory Path: {}".format(self._dirname))

        self._bounding_path = self._dirname.replace('cams_lidars.json', 'camera_lidar_semantic_bboxes')
        print("Bounding path", self._bounding_path)
        self.logger.info("Bounding Path: {}".format(self._bounding_path))

        with open(self._dirname, 'r') as f:
            self._config = json.load(f)

    def undistort_image(self, image_ls, cam_name):
        for img in image_ls:
            image = cv2.imread(img)
            mn, basename = os.path.split(img)
            basename = basename.replace('.jpg', '_undistorted.jpg')
            print("mn , basename", mn, basename)
            print("BASE", basename.replace('.jpg', '_undistorted.jpg'))
            undistorted_img_path = os.path.join(mn, basename)

            if cam_name in ['front_left', 'front_center',
                            'front_right', 'side_left',
                            'side_right', 'rear_center']:
                # get parameters from config file

                intr_mat_undist = np.asarray(self._config['cameras'][cam_name]['CamMatrix'])

                intr_mat_dist = np.asarray(self._config['cameras'][cam_name]['CamMatrixOriginal'])
                dist_parms = np.asarray(self._config['cameras'][cam_name]['Distortion'])
                lens = self._config['cameras'][cam_name]['Lens']

                if (lens == 'Fisheye'):
                    fisheye = cv2.fisheye.undistortImage(image, intr_mat_dist, D=dist_parms, Knew=intr_mat_undist)
                    imgs = fisheye
                elif (lens == 'Telecam'):
                    undist_image_front_center = cv2.undistort(image, intr_mat_dist, distCoeffs=dist_parms,
                                                              newCameraMatrix=intr_mat_undist)
                    cv2.imwrite(undistorted_img_path, undist_image_front_center)
                    imgs = undist_image_front_center
                else:
                    cv2.imwrite(undistorted_img_path, image)
                    imgs = image
            else:
                cv2.imwrite(undistorted_img_path, image)
                imgs = image

        return imgs

    def discover_bounding_box(self):
        bb = BoundingBox(self._bounding_path)

        img_list_dist = []
        box_lst = []

        for p in iglob(os.path.join(self._bounding_path, '*', 'label3D', 'cam_front_center', '*.json'), recursive=True):
            boxes = bb.read_bounding_boxes(p)
            box_lst.append(boxes)

            img_path = p.replace('label3D', 'camera')
            img_path = img_path.replace('.json', '.jpg')

            img_list_dist.append(img_path)
            self._all_images = img_list_dist

        return box_lst, img_list_dist

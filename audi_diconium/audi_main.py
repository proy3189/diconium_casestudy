from audi_diconium.core.audi_json_parser import *
from audi_diconium.util import *

if __name__ == "__main__":
    logger = setup_logging("main.log")
    logger.info("Started with main exectution")
    path = r"F:\ROY\Jobs\Diconium\data\a2d2\cams_lidars.json"
    ap = AudiConfigParser(path)  # parse json and store information
    box, img_lst = ap.discover_bounding_box()
    ap.undistort_image(img_lst, "front_center")

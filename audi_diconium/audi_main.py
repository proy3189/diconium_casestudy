from audi_diconium.core.audi_json_parser import *
from audi_diconium.util import *
from argparse import ArgumentParser



def get_arguments():
    args =parse_arguments()
    logger = setup_logging("main.log")
    logger.info("Started with main exectution")
    # path = r"F:\ROY\Jobs\Diconium\audi\roy\data\a2d2\cams_lidars.json"
    path = args.dataset_path
    ap = AudiConfigParser(path)  # parse json and store information
    box, img_lst = ap.discover_bounding_box()
    ap.undistort_image(img_lst, "front_center")


def parse_arguments():
    parser = ArgumentParser(description=('Execute task'))
    parser.add_argument('dataset_path', type=str, help='path to the a2d2 dataset root folder')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    get_arguments()



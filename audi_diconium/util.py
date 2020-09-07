import logging
import os
import inspect

__all__ =["create_dir_recursively", "setup_logging"]

def create_dir_recursively(path, is_file_path= False):
    if is_file_path:
        path = os.path.dirname(path)
    if not os.path.exists(path):
        path = os.makedirs(path, exist_ok=True)

    return path


def setup_logging(logpath=None, level= logging.INFO):
    if logpath is None:
        dirname = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        print("dirname", dirname)
        dirname = os.path.join(dirname, "logs", "logs.logs")

        print("AP dirname", dirname)
        create_dir_recursively(dirname, is_file_path=True)


    logging.basicConfig(filename=logpath, level=level,format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('SetupLogger')
    logger.info("Log file path: {}".format(logpath))
    return logger





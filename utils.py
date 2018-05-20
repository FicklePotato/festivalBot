import os
import time

ROOT_OUT_PATH = r"C:\Projects\festivalBot\media"


def gen_out_path(file_type="png", group_id="Default", curr_time=None):
    out_dir = os.path.join(ROOT_OUT_PATH, group_id)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    curr_time = int(time.time()) if curr_time is None else curr_time
    filename = "{0}.{1}".format(curr_time, file_type)
    full_path = os.path.join(out_dir, filename)
    while os.path.isfile(full_path):
        full_path = gen_out_path(file_type, group_id, "{0}_1".format(curr_time))
    return full_path

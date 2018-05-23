import os
import time
import sched
from activity_logger import dump_groups, JSON_PATH

ROOT_OUT_PATH = r"C:\Projects\festivalBot\media"
DUMP_TIME = 10

# TODO: get a group object and generate a path
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


def single_dump(s, groups):
    dump_groups(JSON_PATH, groups)
    # do your stuff
    s.enter(DUMP_TIME, 1, single_dump, (s, groups))


def enter_dump_cycle(groups):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(DUMP_TIME, 1, single_dump, (s, groups))
    s.run()

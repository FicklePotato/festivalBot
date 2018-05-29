import os
import time
import sched
from activity_logger import dump_groups, JSON_PATH

ROOT_OUT_PATH = r"media"
DUMP_TIME = 10


def gen_out_path(file_type="png", group_id="Default", prefix=None):
    out_dir = os.path.join(ROOT_OUT_PATH, group_id)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    prefix = int(time.time()) if prefix is None else prefix
    filename = "{0}.{1}".format(prefix, file_type)
    full_path = os.path.join(out_dir, filename)
    while os.path.isfile(full_path):
        full_path = gen_out_path(file_type, group_id, "{0}_1".format(prefix))
    return full_path


def single_dump(s, groups):
    dump_groups(JSON_PATH, groups)
    # do your stuff
    s.enter(DUMP_TIME, 1, single_dump, (s, groups))


def enter_dump_cycle(groups):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(DUMP_TIME, 1, single_dump, (s, groups))
    s.run()

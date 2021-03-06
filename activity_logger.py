import json
import os
from consts import *


class Group(object):
    def __init__(self, id, completed_missions, title):
        self.id = id
        self.completed_missions = completed_missions
        self.title = title

    def get_score(self):
        return sum(MISSION_SCORE[m] for m in self.completed_missions)

    def complete_mission(self, mission):
        if mission in MISSION_SCORE and mission not in self.completed_missions:
            self.completed_missions.append(mission)
            return True


def dump_groups(json_path, groups):
    with open(json_path, "w") as f:
        json.dump({k: (groups[k].completed_missions, groups[k].title) for k in groups}, f)


def load_groups(json_path):
    if not os.path.isfile(json_path):
        return []
    with open(json_path, "r") as f:
        groups = json.load(f)
    return {int(k): Group(int(k), groups[k][MISSION_LOC], groups[k][TITLE_LOC]) for k in groups}

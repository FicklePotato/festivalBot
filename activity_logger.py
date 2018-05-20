import json
import os

MAX_TIMES = 3
MISSION_SCORE = {1: 1, 2: 2, 3: 1}
ID_LOC = 0
USER_LOC = 1
TIMES_CHANGED_LOC = 1
JSON_PATH = r"C:\Projects\festivalBot\groups.json"


class User(object):
    def __init__(self, id, group, times_changed=0):
        self.id = id
        self.group = group
        self.times_changed = times_changed

    def change_group(self, new_group):
        if new_group.id != self.group.id and self.times_changed < MAX_TIMES:
            self.group = new_group
            self.times_changed += 1
            return True

    def __str__(self):
        return "({0}, {1}, {2})".format(self.id, self.group.id, self.times_changed)


class Group(object):
    def __init__(self, id, users, completed_missions=list()):
        self.id = id
        self.users = users
        self.completed_missions = completed_missions

    def add_user(self, user):
        if user.id not in [u.id for u in self.users]:
            self.users.append(user)
            user.group = self
            return True

    def get_score(self):
        return sum(MISSION_SCORE[m] for m in self.completed_missions)

    def complete_mission(self, mission):
        if mission in MISSION_SCORE and mission not in self.completed_missions:
            self.completed_missions.append(mission)
            return True

    def get_json_format(self):
        return self.id, [(user.id, user.times_changed)for user in self.users], self.completed_missions

    @staticmethod
    def from_json(json_data):
        new_group = Group(json_data[ID_LOC], [])
        for user in json_data[USER_LOC]:
            new_group.users.append(User(user[ID_LOC], new_group, user[TIMES_CHANGED_LOC]))
        return new_group


def dump_groups(json_path, groups):
    with open(json_path, "w") as f:
        json.dump([g.get_json_format() for g in groups], f)


def load_groups(json_path):
    if not os.path.isfile(json_path):
        return []
    with open(json_path, "r") as f:
        groups = json.load(f)
    return [Group.from_json(g) for g in groups]

import os
import json

class MongoDB:
    def __init__(self, path) -> None:
        with open(path) as json_file:
            self.data = json.load(json_file)

    def get_events_by_date_type(self, date, type):
        res_lst = []
        for event in self.data:
            if True:
                res_lst.append(event)
        return res_lst
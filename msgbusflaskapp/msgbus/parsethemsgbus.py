import re, json
from collections import defaultdict
import builtins


class Worker:
    def __init__(self, filename):
        self.filename = filename
        self.content = None
        self.read_file()

    def read_file(self):
        with open(self.filename, "r",encoding='UTF8') as myfile:
            self.content = myfile.readlines()

    @staticmethod
    def match(line, pattern):
        if re.match(f".*{pattern}.*", string=line):
            return line


class Gzflt(Worker):
    def __init__(self, filename):
        Worker.__init__(self, filename=filename)
        self.filename = filename
        self.gzflt = []
        self.pids = []

    def get_gzflt(self):
        matched_lines = []
        for cont in self.content:
            regex = self.match(cont, "on gzflt")
            if regex:
                content = list(re.split("replies false: ", str(regex)))
                if len(content) > 1:
                    matched_lines.append(content[1])
        return matched_lines

    def convert_to_dictionary(self):
        matched_lines = self.get_gzflt()
        for line in matched_lines:
            current_json = json.loads(line)
            current_json['pid'] = (current_json['pid']).split(' ')[1]
            current_json['file_path'] = (current_json['file_path']).split(' ')[1]
            self.gzflt.append(current_json)

    def get_pids(self):
        self.convert_to_dictionary()
        for gzlft_item in self.gzflt:
            self.pids.append(gzlft_item['pid'])


class EdrSensor(Worker):
    def __init__(self, filename):
        Worker.__init__(self, filename=filename)
        self.edrs = []

    def get_edrSensor(self):
        for line in self.content:
            regex = self.match(line, 'on edrsensor')
            if regex:
                content = list(re.split("on edrsensor : ", str(regex)))
                if len(content) > 1:
                    self.edrs.append(json.loads(content[1]))


class Regmon(Worker):
    def __init__(self, filename):
        Worker.__init__(self, filename)
        self.filename = filename
        self.regmons = []

    def get_regmons(self):
        for line in self.content:
            regex = self.match(line, 'on regmon')
            if regex:
                content = list(re.split("on regmon : ", str(regex)))
                if len(content) > 1:
                    self.regmons.append(json.loads(content[1]))


def regmons_edrs_with_pid(gzflt, regmons, edrsensors):
    pids_and_regmons_edr = defaultdict(list)
    for pid in gzflt.pids:
        for regmon in regmons.regmons:
            for index_regmon, item_regmon in regmon.items():
                if re.match(".*" ".*", item_regmon):
                    if len((str(item_regmon).split(" "))) > 1:
                        regmon[index_regmon] = (str(item_regmon).split(" "))[1]
            if regmon['pid'] == pid:
                pids_and_regmons_edr[pid].append(regmon)
        for edr in edrsensors.edrs:
            for index_edr, item_edr in edr.items():
                if re.match(".*" ".*", item_edr):
                    if len((str(item_edr).split(" "))) > 1:
                        edr[index_edr] = item_edr.split(" ")[1]
            if edr['pid'] == pid:
                pids_and_regmons_edr[pid].append(edr)
    fields = set()
    for vector in pids_and_regmons_edr.values():
        for item in vector:
            for field in item.keys():
                fields.add(field)

    return pids_and_regmons_edr, fields


def get_for_filename_all_pids(filename):
    mygzflt = Gzflt(filename)
    mygzflt.get_pids()
    return mygzflt.gzflt


def make_everything(filename):
    myregmon = Regmon(filename)
    mygzflt = Gzflt(filename)
    myedr = EdrSensor(filename)

    myregmon.get_regmons()
    mygzflt.get_pids()
    myedr.get_edrSensor()

    return regmons_edrs_with_pid(mygzflt, myregmon, myedr)


if __name__ == '__main__':
    pass
    # myregmon = Regmon("C:/Users/mrezmerita/Downloads/MSGBUS_11.log")
    # myregmon.get_regmons()
    #
    # mygzflt = Gzflt("C:/Users/mrezmerita/Downloads/MSGBUS_11.log")
    # mygzflt.get_pids()
    #
    # myedr = EdrSensor("C:/Users/mrezmerita/Downloads/MSGBUS_11.log")
    # myedr.get_edrSensor()
    #
    # get_events_for_pid(regmons_edrs_with_pid(mygzflt, myregmon,myedr),2484)

    # get_for_pid_filename_all_events("Ceva")

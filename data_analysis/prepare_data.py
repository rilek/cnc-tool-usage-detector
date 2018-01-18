"""Data preparation module"""

import os
import re
import csv
from shutil import copy2
import numpy as np
import pandas as pd
from config.config import CONFIG as c

def mkdir_if_not_exists(dirs):
    """A"""

    if not os.path.exists(dirs):
        os.makedirs(dirs)

def prepare_dirs(dirs):
    """A"""

    for _dir in dirs:
        mkdir_if_not_exists(_dir)
        mkdir_if_not_exists(_dir + "ostre")
        mkdir_if_not_exists(_dir + "tepe")


def init():
    """Main function"""

    directory = c["NEW_TRAIN_FILES_DIR"]
    ver = c["VER"]
    get_pt_dir = lambda pt: directory + "pt" + pt + "/" + ver
    files_list = os.listdir(get_pt_dir('0'))

    # prepare_dirs([get_pt_dir('1'), get_pt_dir('2'), get_pt_dir('3')])
    mkdir_if_not_exists(directory + "final/" + ver)
    indexes = [0, 0] # sharp_i, blunt_i

    for file_name in files_list:
        p = re.search('(?<=P)(\d)+', file_name).group()

        if not p == '0':
            file_class = 1 if p == '2' else 0
            fil = pt2_2(file_name,get_pt_dir('0'))
            pt3_2(fil, file_class, directory + "final/" + ver, indexes)

    # pt1(files_list, get_pt_dir('0'), directory + "final/" + ver)
    # pt2(classes, get_pt_dir('1'), get_pt_dir('2'))
    # pt3(classes, get_pt_dir('2'), get_pt_dir('3'))
    # pt4(classes, get_pt_dir('3'), directory + "final/" + ver)



def pt1(files_list, pt0_dir, final_dest):
    """Groups files in 2 directories: 'tepe' and 'ostre'"""

        # if p == '2':
        #     copy2(pt0_dir + file_name, pt1_dir + "Tepe_" + ts + ".txt")
        # elif not p == '0':
        #     copy2(pt0_dir + file_name, pt1_dir + "Ostre_D" + ts + ".txt")

def pt2_2(file_name, final_dest):
    """A"""

    results = []
    with open(final_dest + file_name) as fil:
        for line in fil:
            splitted_line = line.split(",")
            sensor = splitted_line[0]
            measurements = splitted_line[8:][0::2]
            results.append([sensor] + measurements)
    return results

def pt3_2(fil, file_class, final_dest, indexes):
    """A"""

    acc_signal = []
    mic_signal = []

    for line in fil:
        sensor = line[0]
        measurements = line[1:]

        if sensor == "1":
            acc_signal.extend(measurements)
        elif sensor == "2":
            mic_signal.extend(measurements)

        if len(mic_signal) >= 16000 and len(mic_signal) == len(acc_signal):
            file_name = "Tepe_" if file_class == 1 else "Ostre"

            with open(final_dest+file_name+str(indexes[file_class])+".csv", "w+", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                for row in np.matrix([acc_signal, mic_signal]).T.tolist():
                    writer.writerow(row)

            acc_signal = []
            mic_signal = []

            indexes[file_class] = indexes[file_class] + 1


def pt2(dirs, pt1_dir, pt2_dir):
    """Cleans up files from tepe and ostre directories:
    Removes from lines unnecessary data. Leaves only sensor number and measurements"""

    for _dir in dirs:
        __dir = pt1_dir + _dir
        __dir2 = pt2_dir + _dir
        files_list = os.listdir(__dir)
        for file_name in files_list:
            results = []
            with open(__dir + file_name) as fil:
                for line in fil:
                    splitted_line = line.split(",")
                    sensor = splitted_line[0]
                    measurements = splitted_line[8:][0::2]
                    results.append(",".join([sensor] + measurements))
            with open(__dir2 + file_name, 'w+') as fil:
                fil.write(str("\n".join(results)))

def pt3(dirs, pt2_dir, pt3_dir):
    """Groups measurements based on sensor number.
    After each group is 16000 long, its saved to new (csv?) file"""
    for _dir in dirs:
        __dir2 = pt2_dir + _dir
        __dir3 = pt3_dir + _dir
        name_prefix = "Ostre_" if _dir == "ostre/" else "Tepe_"
        acc_i = 0
        acc_signal = []
        mic_signal = []
        for file_name in os.listdir(__dir2):

            with open(__dir2 + file_name) as fil:
                for line in fil:
                    line = line.split(",")
                    sensor = line[0]
                    measurements = map(int, line[1:])
                    # print(sensor)
                    if sensor == "1":
                        acc_signal.extend(measurements)
                    elif sensor == "2":
                        mic_signal.extend(measurements)

                    if len(mic_signal) >= 16000 and len(mic_signal) == len(acc_signal):
                        with open(__dir3+name_prefix+str(acc_i)+".csv", "w+", newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=",")
                            for row in np.matrix([acc_signal, mic_signal]).T.tolist():
                                writer.writerow(row)
                            acc_i = acc_i + 1

                        acc_signal = []
                        mic_signal = []

def pt4(dirs, pt3_dir, final_dir):
    """Copies all files to 1 folder"""

    for _dir in dirs:
        __dir3 = pt3_dir + _dir

        for file_name in os.listdir(__dir3):
            copy2(__dir3 + file_name, final_dir)



if __name__ == "__main__":
    init()

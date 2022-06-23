import psutil
import os
from multiprocessing import Process
import numpy as np
import time
import argparse
import sys
import glob


def config_read():
    with open("./config.cfg", 'r') as f:
        lines = f.readlines()

    for line in lines:
        tmp = line.split()
        if tmp[0] == "orb_slam_2_path":
            orb_slam_2_path = tmp[1]
        elif tmp[0] == "img_file_path":
            img_file_path = tmp[1]
    return orb_slam_2_path, img_file_path


def yaml_read():
    yaml_list = glob.glob("./yaml_files/*.yaml")
    return yaml_list


def cpu_percent_show(cpu_usage_total, number_of_cpu_usage_pts):
    cpu_usage = psutil.cpu_percent(interval=0.5, percpu=True)
    for i in range(len(cpu_usage_total)):
        cpu_usage_total[i] += int(cpu_usage[i])
    number_of_cpu_usage_pts.value += 1
    print("\n===============")
    for i, cpu in enumerate(cpu_usage):
        print("cpu", i, " ", cpu)


def kitti_start_func(seq, type, yaml_file_path):
    path_to_orb_slam, img_file_path = config_read()
    seq_txt = ""

    if (seq < 10):
        seq_txt = "0" + str(seq)
    else:
        seq_txt = str(seq)

    if (type == "mono"):
        cc_file = path_to_orb_slam + "/Examples/Monocular/mono_kitti"
    elif (type == "stereo"):
        cc_file = path_to_orb_slam + "/Examples/Stereo/stereo_kitti"
    else:
        print("invalid type: ", type)
        sys.exit()

    voca_file = path_to_orb_slam + "/Vocabulary/ORBvoc.txt"

    img_file = img_file_path + "/" + seq_txt
    kitti_statrt_code = ' '.join(
        [cc_file, voca_file, yaml_file_path, img_file])
    os.system(kitti_statrt_code)


def yaml_split(reference_name):
    type, seq, characteristics = reference_name.split('_')
    seq = int(seq)
    characteristics = characteristics.replace(".yaml", "")
    return type, seq, characteristics


def seq2seqtxt(seq):
    if seq < 10:
        seq_txt = '0' + str(seq)
    else:
        seq_txt = str(seq)
    return seq_txt


def changing_keframe_trajectory_name_mono(reference_name):
    type, seq, characteristics = yaml_split(reference_name)
    seq_txt = seq2seqtxt(seq)

    file_name = type + "_" + seq_txt + "_" + characteristics + ".txt"

    code = "mv KeyFrameTrajectory.txt " + file_name
    os.system(code)
    return file_name


def path_check_deletion(file_name):
    if (os.path.isfile(file_name)):
        os.remove(file_name)


def changing_trajectory_name_stereo(reference_name):
    type, seq, characteristics = yaml_split(reference_name)
    seq_txt = seq2seqtxt(seq)

    file_name = "./stereo_traj/" + type + "_" + \
        seq_txt + "_" + characteristics + ".txt"

    code = "mv CameraTrajectory.txt " + file_name
    os.system(code)
    return file_name


def evo_mono(reference_name, file_name):
    type, seq, characteristics = yaml_split(reference_name)
    seq_txt = seq2seqtxt(seq)

    gt_txt = "./gt_tum/gt_tum_" + seq_txt + ".txt"
    code = "evo_traj tum " + file_name + " " + gt_txt+" -p --plot_mode=xz --ref="\
        + gt_txt + " -as --save_as_tum"

    gt_tum_rm_code = "rm gt_tum_*" + ".tum"
    mv_traj_code = "mv *.tum ./modified_mono_traj/"
    txt_remove_code = "rm *.txt"
    os.system(code)
    os.system(gt_tum_rm_code)
    os.system(mv_traj_code)
    os.system(txt_remove_code)

    modified_traj_name = "./modified_mono_traj/" + type + "_" \
        + seq_txt + "_" + characteristics + ".tum"

    ape_file_path = "./ape_results/" \
        + type + "_" + seq_txt + "_" + characteristics + "_ape.zip"
    rpe_file_path = "./rpe_results/" \
        + type + "_" + seq_txt + "_" + characteristics + "_rpe.zip"

    path_check_deletion(ape_file_path)
    path_check_deletion(rpe_file_path)

    evo_ape_code = "evo_ape tum " + gt_txt + " " + modified_traj_name \
        + " -va --plot_mode xz --save_results " + ape_file_path
    evo_rpe_code = "evo_rpe tum " + gt_txt + " " + modified_traj_name \
        + " -va --plot_mode xz --save_results " + rpe_file_path
    os.system(evo_ape_code)
    time.sleep(1)
    os.system(evo_rpe_code)


def evo_stereo(reference_name, file_name):
    type, seq, characteristics = yaml_split(reference_name)
    seq_txt = seq2seqtxt(seq)

    gt_txt = "./gt_tum/gt_tum_" + seq_txt + ".txt"
    ape_file_path = "./ape_results/" \
        + type + "_" + seq_txt + "_" + characteristics + "_ape.zip"
    rpe_file_path = "./rpe_results/" \
        + type + "_" + seq_txt + "_" + characteristics + "_rpe.zip"

    path_check_deletion(ape_file_path)
    path_check_deletion(rpe_file_path)

    evo_ape_code = "evo_ape tum " + gt_txt + " " + file_name \
        + " -va --plot_mode xz --save_results " + ape_file_path
    evo_rpe_code = "evo_rpe tum " + gt_txt + " " + file_name \
        + " -va --plot_mode xz --save_results " + rpe_file_path
    os.system(evo_ape_code)
    time.sleep(1)
    os.system(evo_rpe_code)


def mv_tum_file():
    code = "mv Key*.tum ./modified_mono_traj && rm ./*.txt && rm ./*.tum"
    os.system(code)

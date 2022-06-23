import psutil
import os
from multiprocessing import Process, Array, Value
import numpy as np
import time
import argparse
import sys
import glob
from tools import tool

'''
path should be checked before use!
'''

# def parse_args():
#     parser = argparse.ArgumentParser(description="orb cpu time")
#     parser.add_argument("--kitti_sequence", type=int,
#                         help="kitti_sequence", default=0)
#     if (len(sys.argv) == 1):
#         # python file opened without any argument
#         parser.print_help()
#         sys.exit(1)
#     args = parser.parse_args()
#     return args


def start():
    yaml_list = tool.yaml_read()
    for yaml_file in yaml_list:
        print("\n=======================yaml_file==========================")
        reference_name = yaml_file.split('/')[-1]
        print(reference_name)
        type, seq, characteristics = tool.yaml_split(reference_name)
        seq_txt = tool.seq2seqtxt(seq)

        check_times = Value('i', 0)
        cpu_usage_total = Array('d', [0] * 8)

        p1 = Process(target=tool.kitti_start_func, args=(seq, type, yaml_file))
        p2 = Process(target=tool.cpu_percent_show, args=(
            cpu_usage_total, check_times))

        p1.start()
        start_time = time.time()
        time.sleep(10)
        print("start now!")
        while (p1.is_alive()):
            if (not p2.is_alive()):
                p2.run()

        cpu_avg_usage = [round(cpu_usage_total[i]
                               / check_times.value, 2) for i in range(len(cpu_usage_total))]
        print("\n\n===========Final CPU average usage=============")
        print(cpu_avg_usage)
        end_time = time.time()

        if type == "mono":
            file_name = tool.changing_keframe_trajectory_name_mono(
                reference_name)
            tool.evo_mono(reference_name, file_name)
            with open("./cpu_mono/"+type+"_"+str(seq)+"_"+characteristics+"_cpu.txt", 'w') as f:
                for cpu in cpu_avg_usage:
                    f.write(str(cpu))
                    f.write(" ")
                f.write("total time: ")
                f.write(str(end_time-start_time))
        else:
            file_name = tool.changing_trajectory_name_stereo(reference_name)
            tool.evo_stereo(reference_name, file_name)
            with open("./cpu_stereo/"+type+"_"+str(seq)+"_"+characteristics+"_cpu.txt", 'w') as f:
                for cpu in cpu_avg_usage:
                    f.write(str(cpu))
                    f.write(" ")
                f.write("total time: ")
                f.write(str(end_time-start_time))
        os.system("mv prof.prof ./prof_file/"+type+"_"
                  + str(seq)+"_"+characteristics+"_prof.prof")


if __name__ == "__main__":
    # args = parse_args()
    # seq = int(args.kitti_sequence)
    start()

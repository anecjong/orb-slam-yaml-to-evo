<div align="center">
  <h1>ORB-SLAM-2, kitti데이터 분석에서 EVO/CPU usage/Profile</h1>
</div>

## **목적**
ORB-SLAM-2에서 YAML 파일의 인자를 수정해가면서 데이터를 얻는 과정이 반복적이고 많은 코드를 반복해서 이용해 결과 데이터 수집에 어려움을 느꼈습니다. 모든 과정들을 한번에 처리하기 위해서 코드를 작성하였습니다.


## **필요한 것들**
리눅스에서 경로 설정을 해두어서 리눅스 환경에서 돌아갑니다.  
[ORB-SLAM-2](https://github.com/raulmur/ORB_SLAM2): OpenCV4 버전을 이용하고 싶은 경우에는 [여기](https://github.com/Windfisch/ORB_SLAM2)  
[easy_profiler](https://github.com/yse/easy_profiler) : profiler  
[evo](https://github.com/MichaelGrupp/evo) : APE, RPE 데이터, monocular일 경우 scale 맞춰줌.  
[psutil](https://pypi.org/project/psutil/): cpu 점유율 관련


## **설정파일**
config.cfg 파일
```
orb_slam_2_path /home/jong/github_utils/ORB_SLAM2_CV4
img_file_path ~/Downloads/data_odometry_gray/dataset/sequences
```
orb_slam_2_path 뒤의 부분을 ORB-SLAM-2가 있는 경로로 설정합니다.  
img_file_path 뒤의 경로는 [kitti 데이터](http://www.cvlibs.net/datasets/kitti/eval_odometry.php)의 odometry data set(grayscale, 22 GB)의 sequences 부분까지 경로를 설정해줍니다.

YAML 파일은 아래와 같은 방식으로 yaml_files안에 넣어줍니다.
```
[mono/stereo]_[sequence number(0~10)]_[characteristics(without _)].yaml
ex)
mono_3_defualt.yaml
stereo_7_threshold30.yaml
```
yaml_files 내의 mono_yaml_files와 stereo_yaml_files에 들어가 있는 부분을 수정하여 작성하는 것을 권장합니다.


## ORB-SLAM-2 내 코드 수정
Examples/Monocular/mono_kitti.cc의 main 함수 하단 부분을 아래와 같이 설정합니다.
```
    // Save camera trajectory
    SLAM.SaveKeyFrameTrajectoryTUM("KeyFrameTrajectory.txt");    
    SLAM.SaveTrajectoryTUM("hi.txt");
    profiler::dumpBlocksToFile("prof.prof");
    return 0;
```

Examples/Stereo/stereo_kitti.cc의 main 함수 하단 부분을 아래와 같이 설정합니다.
```
    // Save camera trajectory
    SLAM.SaveTrajectoryTUM("CameraTrajectory.txt");
    profiler::dumpBlocksToFile("prof.prof");

    return 0;
```
이후 빌드해줍니다.

## **작동방식**
최상단 경로에서 터미널을 실행합니다.
```
$ python3 orb_from_yaml.py
```

yaml 파일에 있는 것들이 모두 실행되며, 아래와 같은 결과물들을 얻을 수 있습니다.
```
.
├── ape_results
│   ├── mono_03_default_ape.zip
│   └── stereo_07_threshold30_ape.zip
├── config.cfg
├── cpu_mono
│   └── mono_3_default_cpu.txt
├── cpu_stereo
│   └── stereo_7_threshold30_cpu.txt
├── gt_tum
│   ├── gt_tum_00.txt
│   ├── gt_tum_01.txt
│   ├── gt_tum_02.txt
│   ├── gt_tum_03.txt
│   ├── gt_tum_04.txt
│   ├── gt_tum_05.txt
│   ├── gt_tum_06.txt
│   ├── gt_tum_07.txt
│   ├── gt_tum_08.txt
│   ├── gt_tum_09.txt
│   └── gt_tum_10.txt
├── modified_mono_traj
│   └── mono_03_default.tum
├── orb_from_yaml.py
├── prof_file
│   ├── mono_3_default_prof.prof
│   └── stereo_7_threshold30_prof.prof
├── README.md
├── rpe_results
│   ├── mono_03_default_rpe.zip
│   └── stereo_07_threshold30_rpe.zip
├── stereo_traj
│   └── stereo_07_threshold30.txt
├── tools
│   ├── __init__.py
│   ├── __pycache__
│   └── tool.py
└── yaml_files
    ├── mono_3_default.yaml
    ├── mono_yaml_files
    ├── stereo_7_threshold30.yaml
    └── stereo_yaml_files

```

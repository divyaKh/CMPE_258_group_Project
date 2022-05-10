# Title: Fitness Tracker - Real Time Action Recognition and Arm Curler Reps Counter 

## Contents

 * [Objective](#Objective)
 * [Folder Structure](#folder-structure)
 * [Steps to run the project](#steps-to-run-the-project)
 * [Dataset](#Dataset)
 * [METHODOLOGY EMPLOYED](### METHODOLOGY EMPLOYED)
 * [Conclusion](#Conclusion)
 * [Contributors](#Contributors)



## Objective







### Folder Structure

```shell
CMPE_258_group_Project/
├── 1_Image_Annotation
│   ├── Convert_to_YOLO_format.py
│   └── README.md      
├── 2_Training
│   ├── Download_and_Convert_YOLO_weights.py
│   ├── src
│   ├── Train_YOLO.py
│   └── README.md 
├── data_preprocessing
│   ├── CustomerChurnPrediction.ipynb
│   └── README.md
└── I3_Inference   
│   ├── Detector.py
│   ├── images 
│   ├── settings.py 
│   └── README.md
└── Data
│   ├── Model_Weights
│   └── Source_Images
└── Utils
│   ├── 
│   └── 
└── Venv
│   ├── 
│   └── 
└──  README.md 
```

### Steps to run the project
1. Clone the project at the location https://github.com/MANJUSHREEBR/CMPE_258_group_Project.git
2. 
## Dataset

https://www.kaggle.com/datasets/niharika41298/yoga-poses-dataset
</br>
 Dataset consists of images of 5 yoga poses. Which are as follows:
 1. Tree Pose
 2. No Pose
 3. Downward Dog Pose 
 4. Goddess Pose
 5. Plank Pose
 6. Warrior Pose

### Contributors

* [Aishwarya Paruchuri](https://github.com/aishwarya95698)
* [Archita Chakraborty](https://github.com/Archita22ind)
* [Manjushree Barike Rajanna](https://github.com/MANJUSHREEBR)
* [Divya Khandelwaal](https://github.com/divyaKh)

### METHODOLOGY EMPLOYED :

To recognize real-time yoga postures, we trained the Yolov3 model on a subset of images exhibiting 5 different yoga stances. We also implemented a counter to keep track of how long the user remains  in the pose. We also used the Mediapipe pose estimation model to add a bicep curl tracker to our fitness app, which employs an ML model to estimate a person's pose from an image or video by calculating the spatial locations of important body joints. We added curl counter logic to this, which calculates the angles between joints and we set a threshold, such as if the arm moves beyond 160 degrees and then below 30 degrees, the repeat counter is incremented.



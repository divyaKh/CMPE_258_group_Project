# Title: Real Time Pose Estimation and Bicep Curl Counter

+<img src="/results/git_pose_estimation.gif?raw=true" width="1000px">
+<img src="/results/git_pose_estimation_1.gif?raw=true" width="1000px">
+<img src="/results/git_arm_curler.gif?raw=true" width="1000px">


## Dataset

https://www.kaggle.com/datasets/niharika41298/yoga-poses-dataset
</br>
Dataset consists of images of 5 yoga poses. Which are as follows:

1.  Tree Pose 
2.  No Pose
3.  Downward Dog Pose
4.  Goddess Pose
5.  Plank Pose
6.  Warrior Pose

## Folder Structure
```shell
cmpe_258_group_project/
├── 1_Image_Annotation
│   ├── Convert_to_YOLO_format.py   
│   └── README.md      
├── 2_Training
│   ├──src
|      ├── keras_yolo3
|          ├── __pycache__
|              ├── yolo.cpython-36.pyc
|              ├── yolo.cpython-37.pyc
|              ├── yolo.cpython-38.pyc
|              ├── yolo.cpython-39.pyc
|          ├── .DS_Store
|          ├── LICENSE
|          ├── README.md
|          ├── .coco_annotation.py
|          ├── convert.py
|          ├── darknet53.cfg
|          ├── kmeans.py
|          ├── train.py
|          ├── train_bottleneck.py
|          ├── voc_annotation.py
|          ├── yolo.py
|          ├── yolo_video.py
|          ├── yolov3-tiny.cfg
|          ├── yolov3.cfg
|      ├── font
|              ├── FiraMono-Medium.otf
|              ├── SIL Open Font License.txt
|      ├── model_data
|              ├── coco_classes.txt
|              ├── voc_classes.txt
|              ├── yolo-tiny_anchors.txt
|              ├── yolo_anchors.txt
|      ├── yolo3
|              ├── __pycache__
|                  ├── __init__.cpython-36.pyc
|                  ├── __init__.cpython-37.pyc
|                  ├── __init__.cpython-38.pyct
|                  ├── model.cpython-36.pyc
|                  ├── model.cpython-37.pyc
|                  ├── model.cpython-38.pyc
|                  ├── utils.cpython-36.pyc
|                  ├── utils.cpython-37.pyc
|                  ├── utils.cpython-38.pyc
|              ├── __init__.py
|              ├── model.py
|              ├── utils.py
│   ├── .DS_Store
│   ├── Download_and_Convert_YOLO_weights.py
|   ├── Train_YOLO.py
|   └── README.md
├── 3_Inference
│   └── README.md
├── Data   
│   ├── Source_Images
|       ├── Training_Images
|       └── .DS_Store
│   ├── .DS_Store
│   └── README.md
├── Utils
├── Results
│   ├── .DS_Store
│   ├── git_arm_curler.gif
│   ├── git_pose_estimation_1.gif
│   └── git_pose_estimation.gif
├──.DS_Store
├── README.md
```

### Contributors

- [Aishwarya Paruchuri](https://github.com/aishwarya95698)
- [Archita Chakraborty](https://github.com/Archita22ind)
- [Divya Khandelwaal](https://github.com/divyaKh)
- [Manjushree Barike Rajanna](https://github.com/MANJUSHREEBR)

## References
- [1] https://blog.insightdatascience.com/how-to-train-your-own-yolov3-detector-from-scratch-224d10e55de

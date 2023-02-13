# Title: Real Time Pose Estimation and Bicep Curl Counter
## CMPE 258 Deep Learning Project

## Demo of the project

<img src="/results/git_pose_estimation.gif?raw=true" width="1000px">
<img src="/results/git_arm_curler.gif?raw=true" width="1000px">
<img src="/results/git_pose_estimation_1.gif?raw=true" width="1000px">

## Objective

To create an application that would prompt the user to choose the type of workout he or she wants to learn. If the user chooses yoga, the app will first recognize the pose and start a timer to record the amount of time the user spends in that position. If the user chooses bicep curl, the application will track the number of repetitions for that exercise.


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

1_Image_Annotation: Scripts and instructions on annotating images

2_Training: Scripts and instructions on training your YOLOv3 model

3_Inference: Scripts and instructions on testing your trained YOLO model on new images and videos

Data: Input Data, Output Data, Model Weights and Results

Utils: Utility scripts used by main scripts

## Steps to run the project

1. pip install -r requirements.txt (in a conda environment yolov4-cpu)

2. conda activate yolov4-cpu

3. Source Train images are already annoted and csv file created in Data folder

4. Under Traing folder run the below commands. This step is required as we cannot share the weights and model file due to their huge size. 
    (Model building took approximately 4-5 hours)

     python Download_and_Convert_YOLO_weights.py
     
     python Train_YOLO.py 
     
     (The final weights are saved in TrainYourOwnYOLO/Data/Model_weights)
     (The final model .h5 file is saved  in TrainYourOwnYOLO/Data/Model_weights)
     
5. Under 3_Inference folder run the below commands:

     python Detector.py
   
     (to detect the test images/imput videos/ web cam testing for Yolo model)

     python main.py

     (to run the UI of the project for Yoga pose detection and Arm curler count reps)
    


### Contributors

- [Aishwarya Paruchuri](https://github.com/aishwarya95698)
- [Archita Chakraborty](https://github.com/Archita22ind)
- [Divya Khandelwaal](https://github.com/divyaKh)
- [Manjushree Barike Rajanna](https://github.com/MANJUSHREEBR)

## References

- https://blog.insightdatascience.com/how-to-train-your-own-yolov3-detector-from-scratch-224d10e55de2
- https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42237.pdf
- https://medium.com/@ilias_mansouri/computer-vision-part-8-pose-estimation-stick-figures-using-ai-33e7dcbf603


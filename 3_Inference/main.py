import cv2
import os
import numpy as np
import pandas as pd
import random
import settings
import sys
import test
import time
import timeit
import mediapipe as mp


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

from timeit import default_timer as timer


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

src_path = os.path.join(get_parent_dir(1), "2_Training", "src")
utils_path = os.path.join(get_parent_dir(1), "Utils")
utils1_path = os.path.join(get_parent_dir(1),"3_Inference", "utils1")

sys.path.append(src_path)
sys.path.append(utils_path)
sys.path.append(utils1_path)

from keras_yolo3.yolo import YOLO, detect_video, detect_webcam


pose_dict = {
    0 : 'TREE POSE',
    1 : 'GODDESS POSE',
    2 : 'DOWNDOG POSE',
    3 : 'PLANK',
    4 : 'NO POSE',
    5 : 'WARRIOR POSE'
}


yolo = YOLO(
    **{
        "model_path": '../Data/Model_Weights/trained_weights_final.h5',
        "anchors_path": '../2_Training/src/keras_yolo3/model_data/yolo_anchors.txt',
        "classes_path": '../Data/Model_Weights/data_classes.txt',
        "score": 0.25,
        "gpu_num": 1,   #TODO
        "model_image_size": (416, 416),
    }
)


class Ui_MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # self.tracker = Sort(settings.sort_max_age, settings.sort_min_hit)
        self.timer_camera = QtCore.QTimer()
        self.setStyleSheet("background-color: DarkOrange;")
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_mode = 0
        self.fps = 0.00
        self.data = {}
        self.memory = {}
        self.joints = []
        self.current = [] #TODO
        self.previous = []
        self.previous_pose = 4
        self.tic = time.time()
        self.toc = time.time()
        self.title = "Fitness Tracker"
        self.setWindowTitle(self.title)
        self.left_counter = 0
        self.right_counter = 0
        self.left_stage = None
        self.right_stage = None

    def set_ui(self):

        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

        # self.button_open_camera = QtWidgets.QPushButton(u'Camera OFF')

        self.button_mode_1 = QtWidgets.QPushButton(u'Yoga Pose Estimation OFF')
        self.button_mode_1.setStyleSheet("background-color : Cornsilk")
        self.button_mode_2 = QtWidgets.QPushButton(u'Arm Curler Reps OFF')
        self.button_mode_2.setStyleSheet("background-color : Cornsilk")

        self.button_close = QtWidgets.QPushButton(u'Quit')
        self.button_close.setStyleSheet("background-color : Cornsilk")

        self.buttons = [self.button_mode_1,self.button_mode_2, self.button_close]
        
        
        for button in self.buttons:
            button.setMinimumHeight(50)
            self.__layout_fun_button.addWidget(button)
    
        self.button_mode_1.setMinimumHeight(50)
        self.button_mode_2.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        self.button_close.move(10, 100)

        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(200, 200)


        self.label_show_camera.setFixedSize(settings.winWidth + 1, settings.winHeight + 1)
        self.label_show_camera.setAutoFillBackground(True)


        self.__layout_fun_button.addWidget(self.label_move)

        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'Real-time Yoga Pose Estimation and Action Recognition System')

    def slot_init(self):

        self.timer_camera.timeout.connect(self.show_camera)
        self.button_mode_1.clicked.connect(self.button_event)
        self.button_mode_2.clicked.connect(self.button_event)
        self.button_close.clicked.connect(self.close)

    def _button_text_reset(self):
        self.button_mode_1.setText(u' Yoga Pose Estimation OFF')
        self.button_mode_2.setText(u'Arm Curler Reps OFF')

    def button_event(self):
        sender = self.sender()
        if sender == self.button_mode_1 and self.timer_camera.isActive():
            if self.__flag_mode != 1:
                self.__flag_mode = 1
                self._button_text_reset()
                self.button_mode_1.setText(u'Yoga Pose Estimation ON')
            else:
                self.__flag_mode = 0
                self.button_mode_1.setText(u'Yoga Pose Estimation OFF')

        elif sender == self.button_mode_2 and self.timer_camera.isActive():
            if self.__flag_mode != 4:
                self.__flag_mode = 4
                self._button_text_reset()
                self.button_mode_2.setText(u'Arm curler ON')
            else:
                self.__flag_mode = 0

        else:
            self.__flag_mode = 0
            self._button_text_reset()
            if self.timer_camera.isActive() == False:
                flag = self.cap.open(self.CAM_NUM)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.winWidth)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.winHeight)
                if flag == False:
                    msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"Please check if the camera and computer are connected correctly",
                                                        buttons=QtWidgets.QMessageBox.Ok,
                                                        defaultButton=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(1)

            else:
                self.timer_camera.stop()
                self.cap.release()
                self.label_show_camera.clear()

    def show_camera(self):
        print("You are in posing window" + str(self.__flag_mode))       
        start = time.time()
        ret, frame = self.cap.read()
        show = frame
        if ret:

            if self.__flag_mode == 1:
                end = time.time()
                self.fps = 1. / (end - start)

                show,predicted_pose, tic_prev = detect_webcam(yolo, self.cap, self.tic)
                if len(predicted_pose) != 0 and predicted_pose[0][4] != self.previous_pose:
                    self.tic = tic_prev
                else:
                    self.tic = time.time()
                print("tic time", time.asctime( time.localtime(self.tic) ))

                print("our prediction",predicted_pose )

                cv2.putText(show, 'FPS: %.2f' % self.fps, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(show, 'Position held for: %.2f' % (time.time()- self.tic), (460, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
                self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

                print('u are in the same position for ', round((time.time()- self.tic), 3), ' seconds')

            elif self.__flag_mode == 4:
                end = time.time()
                self.fps = 1. / (end - start)
                self.armCurler()

    def _calculate_angle(self,a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle


    def armCurler(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            ret, frame = self.cap.read()
            image = frame

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angle
                left_angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle = self._calculate_angle(right_shoulder, right_elbow, right_wrist)


                # Visualize angle
                cv2.putText(image, str(left_angle),
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                cv2.putText(image, str(right_angle),
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # Curl counter logic
                if left_angle > 160:
                    self.left_stage = "left down"
                if left_angle < 30 and self.left_stage == 'left down':
                    self.left_stage = "left up"
                    self.left_counter += 1
                    print(self.left_counter)

                if right_angle > 160:
                    self.right_stage = "right down"
                if right_angle < 30 and self.right_stage == 'right down':
                    self.right_stage = "right up"
                    self.right_counter += 1
                    print(self.right_counter)


            except:
                pass

            self.BLACK = (0, 0, 0)
            self.WHITE = (255, 255, 255)
            self.LEFT_REPS_TEXT_PLACEMENT = (15, 30)
            self.RIGHT_REPS_TEXT_PLACEMENT = (900, 30)
            self.LEFT_COUNTER_PLACEMENT = (50, 60)
            self.RIGHT_COUNTER_PLACEMENT = (900, 60)


            self.LEFT_STAGE_TEXT_PLACEMENT = (15, 100)
            self.RIGHT_STAGE_TEXT_PLACEMENT = (900, 100)
            self.LEFT_STAGE_PLACEMENT = (50, 130)
            self.RIGHT_STAGE_PLACEMENT = (900, 130)


            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (1200, 150), (245, 117, 16), -1)

            # Rep data
            cv2.putText(image, 'LEFT REPS', self.LEFT_REPS_TEXT_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.BLACK, 1, cv2.LINE_AA)
            cv2.putText(image, str(self.left_counter),
                        self.LEFT_COUNTER_PLACEMENT ,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, self.WHITE, 2, cv2.LINE_AA)

            cv2.putText(image, 'RIGHT REPS', self.RIGHT_REPS_TEXT_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.BLACK, 1, cv2.LINE_AA)
            cv2.putText(image, str(self.right_counter),
                        self.RIGHT_COUNTER_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, self.WHITE, 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'LEFT STAGE', self.LEFT_STAGE_TEXT_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.BLACK, 1, cv2.LINE_AA)
            cv2.putText(image, self.left_stage,
                        self.LEFT_STAGE_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, self.WHITE, 2, cv2.LINE_AA)

            cv2.putText(image, 'RIGHT STAGE', self.RIGHT_STAGE_TEXT_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.BLACK, 1, cv2.LINE_AA)
            cv2.putText(image, self.right_stage,
                        self.RIGHT_STAGE_PLACEMENT,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, self.WHITE, 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=1,
                                                             circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=1, circle_radius=2)
                                      )

            show = image
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"closure", u"close")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'Sure')
        cancel.setText(u'Cancel')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()
            print("System exited.")



if __name__ == "__main__":
    print("Load all models done!")
    print("The system starts ro run.")
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
    

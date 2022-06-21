import logging

from django.shortcuts import render
from django.http import HttpResponse
from teachers.models import TestObjective
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
import cv2
import mediapipe
from datetime import datetime
from .models import ProctoringLog
import torch

# detection_categories = {"tvmonitor": 1, "laptop": 1, "cell phone": 1, "book": 1}
# yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

mp_face_detection = mediapipe.solutions.face_detection
mp_drawing = mediapipe.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5)


def dashboard(request):
    return render(request, 'students/dashboard.html')


def test_login(request):
    return render(request, 'students/test-login.html')


def give_test_objective(request):
    objective_questions = TestObjective.objects.filter(test_id="tangible-pogona")
    context = {"objective_questions": objective_questions}
    return render(request, 'students/give-test-obj.html', context=context)


def give_test_subjective(request):
    return render(request, 'students/give-test-obj.html')


def exam_history(request):
    return render(request, 'students/dashboard.html')


def gen(camera):
    count = 0
    while True:
        frame = camera.get_frame()
        # print(org_frame.shape)
        flag, frame, count = get_results(frame, count)
        if flag == True:
            # print("WOOOOOOO FASSA ",flag)

            frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[0, 0, 255])
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')


def video_stream(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

import base64
def get_result(image, count):
    violate = False
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    now = datetime.now()
    curr_time = now.strftime("%H_%M_%S")
    # model=get_model()
    # yl=False
    # predictions = yolo_model(image)
    # results_ = predictions.pandas().xyxy[0].to_dict(orient="records")
    # for detection in results_:
    #     name = detection["name"]
    #     con = detection['confidence']
    #     if name in detection_categories and con > 0.4:
    #         yl=True

    if type(results.detections) == type(None) or len(results.detections) != 1:  # or yl:
        if count > 10:
            print("screen shot saved ", curr_time)
            image_in_b64 = base64.b64encode(image)
            proctoring_log = ProctoringLog()
            proctoring_log.image = image_in_b64
            proctoring_log.test_id = "test_id"
            proctoring_log.flag = "person on in window or any other flag"
            proctoring_log.student_id = "lakshya"
            proctoring_log.save()


            violate = True
            count = 0
        count += 1

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # if results.detections:
    #     for detection in results.detections:
    #         mp_drawing.draw_detection(image, detection)
    return image, violate, count


def get_results(frame, count):
    frame, violate, count = get_result(frame, count=count)
    return violate, frame, count

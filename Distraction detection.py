import cv2
import mediapipe as mp
import time
import math
import winsound
import threading

# ==============================
# إعداد MediaPipe
# ==============================
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# ==============================
# إعدادات كشف النعاس والتشتت
# ==============================
EAR_THRESHOLD = 0.22

DROWSY_TIME = 2.0
DISTRACTION_TIME = 3.0

eye_closed_start = None
distraction_start = None

alarm_on = False


# ==============================
# صفارة الإنذار
# ==============================
def alarm():
    global alarm_on

    while alarm_on:
        winsound.Beep(2500, 1000)


# ==============================
# حساب EAR
# ==============================
def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def EAR(eye_points):
    A = euclidean(eye_points[1], eye_points[5])
    B = euclidean(eye_points[2], eye_points[4])
    C = euclidean(eye_points[0], eye_points[3])

    if C == 0:
        return 0

    return (A + B) / (2.0 * C)


# ==============================
# تشغيل الكاميرا
# ==============================
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
) as face_mesh:

    prev_time = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("فشل في قراءة الكاميرا")
            break

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb_frame)

        status_text = "ATTENTIVE"
        status_color = (0, 255, 0)

        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:

                img_h, img_w, _ = frame.shape

                mesh_points = [
                    (
                        int(point.x * img_w),
                        int(point.y * img_h)
                    )
                    for point in face_landmarks.landmark
                ]

                # رسم نقاط العين
                for idx in LEFT_EYE + RIGHT_EYE:
                    cv2.circle(
                        frame,
                        mesh_points[idx],
                        2,
                        (0, 255, 0),
                        -1
                    )

                # رسم شبكة الوجه
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=
                    mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )

                # ==========================
                # حساب EAR
                # ==========================
                left_eye_pts = [
                    mesh_points[p]
                    for p in LEFT_EYE
                ]

                right_eye_pts = [
                    mesh_points[p]
                    for p in RIGHT_EYE
                ]

                left_ear = EAR(left_eye_pts)
                right_ear = EAR(right_eye_pts)

                ear = (left_ear + right_ear) / 2

                cv2.putText(
                    frame,
                    f"EAR: {ear:.2f}",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

                # ==========================
                # كشف النعاس
                # ==========================
                if ear < EAR_THRESHOLD:

                    if eye_closed_start is None:
                        eye_closed_start = time.time()

                    closed_duration = (
                        time.time()
                        - eye_closed_start
                    )

                    if closed_duration > DROWSY_TIME:

                        status_text = "DROWSINESS ALERT"
                        status_color = (0, 0, 255)

                        if not alarm_on:
                            alarm_on = True

                            threading.Thread(
                                target=alarm,
                                daemon=True
                            ).start()

                else:
                    eye_closed_start = None

                # ==========================
                # كشف التشتت
                # ==========================
                nose = mesh_points[1]

                center_x = img_w // 2

                if abs(nose[0] - center_x) > 120:

                    if distraction_start is None:
                        distraction_start = time.time()

                    distracted_duration = (
                        time.time()
                        - distraction_start
                    )

                    if distracted_duration > DISTRACTION_TIME:

                        status_text = "DISTRACTION ALERT"
                        status_color = (0, 0, 255)

                        if not alarm_on:
                            alarm_on = True

                            threading.Thread(
                                target=alarm,
                                daemon=True
                            ).start()

                else:
                    distraction_start = None

                # إيقاف الصفارة عند عودة الانتباه
                if (
                    ear >= EAR_THRESHOLD
                    and abs(nose[0] - center_x) <= 120
                ):
                    alarm_on = False

        else:
            alarm_on = False

        # ==========================
        # عرض الحالة
        # ==========================
        cv2.putText(
            frame,
            status_text,
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            status_color,
            3
        )

        # ==========================
        # FPS
        # ==========================
        curr_time = time.time()

        fps = 1 / (curr_time - prev_time) \
            if prev_time != 0 else 0

        prev_time = curr_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        cv2.imshow(
            "Driver Monitoring System",
            frame
        )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
import os
import sys
import time
import math
import keyboard
import cv2

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar2 import QLabsQCar2
from qvl.real_time import QLabsRealTime

# ─────────────────────────────
# LOAD FACE + EYE DETECTORS
# ─────────────────────────────
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# ─────────────────────────────
# SETUP QCAR
# ─────────────────────────────
def setup():
    os.system('cls')

    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")

    if not qlabs.open("localhost"):
        print("Connection failed")
        sys.exit(1)

    print("Connected")

    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()
    time.sleep(1)

    car = QLabsQCar2(qlabs)
    car.spawn_id(
    actorNumber=0,
    location=[1, 2, 0],
    rotation=[0, 0, 0],
    scale=[1, 1, 1],   # REQUIRED
    waitForConfirmation=True
)

    time.sleep(2)
    return car


# ─────────────────────────────
# MAIN LOOP
# ─────────────────────────────
def run(car):
    cap = cv2.VideoCapture(0)

    SPEED = 1.0
    TURN = 0.3

    eye_closed_frames = 0
    DROWSY_THRESHOLD = 10   # frames

    print("\nControls: Arrow keys | ESC to quit\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not working")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        eyes_detected = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) > 0:
                eyes_detected = True

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

        # ── DROWSINESS LOGIC ──
        if not eyes_detected:
            eye_closed_frames += 1
        else:
            eye_closed_frames = 0

        drowsy = eye_closed_frames > DROWSY_THRESHOLD

        # ── KEYBOARD ──
        forward = 0.0
        turn = 0.0

        if not drowsy:  # ONLY DRIVE IF AWAKE
            if keyboard.is_pressed('up'):
                forward = SPEED
            elif keyboard.is_pressed('down'):
                forward = -SPEED

            if keyboard.is_pressed('left'):
                turn = -TURN
            elif keyboard.is_pressed('right'):
                turn = TURN
        else:
            cv2.putText(frame, "DROWSY! STOPPING CAR", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        # ── CONTROL CAR ──
        car.set_velocity_and_request_state(

            forward, turn,
            False, False, False, False, False
        )

        # ── DISPLAY ──
        cv2.imshow("Driver Monitor", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

        time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()

    car.set_velocity_and_request_state(0, 0, False, False, False, False, False)


# ─────────────────────────────
# MAIN
# ─────────────────────────────
if __name__ == "__main__":
    car = setup()
    run(car)

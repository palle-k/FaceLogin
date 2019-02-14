#!/usr/local/bin/python3

import face_recognition
import cv2
import keyring
import getpass
import numpy as np
import base64
import time
# noinspection PyPackageRequirements
import Quartz
import os


if __name__ == '__main__':
    password = keyring.get_password('face_login_password', getpass.getuser())
    enc_bytes = keyring.get_password('face_login_encoding', 'face_encoding')
    ref_encoding = np.frombuffer(base64.b64decode(bytes(enc_bytes, 'ascii')), dtype=np.float32)

    print("Started.")

    while True:
        time.sleep(2)
        # noinspection PyUnresolvedReferences
        d: dict = Quartz.CGSessionCopyCurrentDictionary()
        if 'CGSSessionScreenIsLocked' in d.keys():
            capture = cv2.VideoCapture(0)
            for _ in range(15):
                _ = capture.read()
            _, img = capture.read()
            capture.release()

            if img is None:
                continue

            encodings = face_recognition.face_encodings(img)

            for encoding in encodings:
                dist = np.linalg.norm(encoding - ref_encoding)

                if dist < 0.4:
                    print("UNLOCKED")
                    os.system(f'osascript -e \'tell application "System Events" to keystroke "{password}"\'')
                    os.system(f'osascript -e \'tell application "System Events" to key code 36\'')
                    time.sleep(10)

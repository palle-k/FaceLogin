import keyring
import cv2
import numpy as np
import face_recognition
import getpass
import base64


if __name__ == '__main__':
    print("FaceLogin Setup")
    login_password = getpass.getpass(prompt='Login Password: ')

    print("Step in front of the camera.")

    key = 0
    img = None
    encodings = None

    while key not in {ord('y'), ord('Y')}:
        capture = cv2.VideoCapture(0)
        for i in range(0, 60):
            if i % 20 == 0:
                print((60 - i) // 20)
            _ = capture.read()
        print(0)

        _, img = capture.read()
        capture.release()

        encodings = face_recognition.face_encodings(img)

        if len(encodings) == 1:
            print("Is this a good image? [y/N]")
            cv2.imshow("Face Image", img)
            key = cv2.waitKey()
        else:
            print("Multiple faces in image, trying again.")

    keyring.set_password('face_login_encoding', 'face_encoding', str(base64.b64encode(encodings[0].astype(np.float32)), 'ascii'))
    keyring.set_password('face_login_password', getpass.getuser(), login_password)
    print("Success.")

import concurrent.futures
import threading

import cv2


class FacialRecognitionService:
    face_cascade_classifier = None

    def __init__(self):
        self.face_cascade_classifier = \
            cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def contains_face(self, image_path,):
        """
        Returns true if the image at image_path contains a face

        :param image_path: String path to image
        :return: boolean
        """
        color_img = cv2.imread(image_path)
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade_classifier.detectMultiScale(
            gray_img,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        return len(faces) > 0, faces

    def show_faces_and_get_input(self, image, faces):
        """
        This is janky but it doesnt need to be any better for now
        :param image: The image path to show
        :param faces: The faces to show
        :return: The files new name
        """
        color_img = cv2.imread(image)

        for (x, y, w, h) in faces:
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        resized_img = self.resize_with_aspect_ratio(color_img, height=960)

        cv2.imshow("Faces found", resized_img)
        cv2.waitKey(500)

        try:
            return input("Enter a new filename or 'no' to use the existing name: ")
        except EOFError:
            return None

    def resize_with_aspect_ratio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        From https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
        """
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)

from app.services.contracts import FaceDetector, FaceFactory
from app.services.implementations.DlibFaceDetector import DlibFaceDetector


class DlibModel(FaceFactory):
    def get_detector(self) -> FaceDetector:
        return DlibFaceDetector()
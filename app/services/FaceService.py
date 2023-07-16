from app.services.contracts import FaceDetector
from app.services.implementations import DlibModel


class FaceService:
    """Face service"""

    @staticmethod
    def get_detector(face_model: str = 'dlib') -> FaceDetector:
        """_summary_

        Args:
            face_model (str, optional): _description_. Defaults to 'ssd'.

        Returns:
            FaceFactory: _description_
        """
        factories = {
            "dlib": DlibModel()
        }
        return factories[face_model].get_detector()

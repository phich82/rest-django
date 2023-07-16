from abc import ABC, abstractmethod

from app.services.contracts import FaceDetector


class FaceFactory(ABC):
    """Face factory"""

    @abstractmethod
    def get_detector(self) -> FaceDetector:
        """ Returns new face detector """

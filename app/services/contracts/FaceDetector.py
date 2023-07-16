from abc import ABC, abstractmethod


class FaceDetector(ABC):
    """Detect face

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    def change_orient(self, image, rotate_interval):
        """_summary_

        Args:
            image (_type_): _description_
            rotate_interval (_type_): _description_
        """
        pass

    @abstractmethod
    def find_face(self, image):
        """_summary_

        Args:
            image (_type_): _description_
        """
        pass

    @abstractmethod
    def rotate_bound(self, image, angle):
        """_summary_

        Args:
            image (_type_): _description_
            angle (_type_): _description_
        """
        pass

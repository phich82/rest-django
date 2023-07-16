from app.services.contracts import FaceDetector


class DlibFaceDetector(FaceDetector):
    """_summary_

    Args:
        FaceDetector (_type_): _description_
    """

    def test(self):
        """_summary_
        """
        print("DlibFaceDetector:test")

    def change_orient(self, image, rotate_interval):
        print("DlibFaceDetector:change_orient")

    def find_face(self, image):
        print("DlibFaceDetector:find_face")

    def rotate_bound(self, image, angle):
        print("DlibFaceDetector:rotate_bound")

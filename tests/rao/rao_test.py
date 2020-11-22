import unittest


class RaoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from gooutsafe import create_app
        cls.app = create_app()

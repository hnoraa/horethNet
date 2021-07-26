# UPDATE: https://stackoverflow.com/questions/60981061/flask-db-init-leads-to-keyerror-migrate
import unittest

def test():
    """Runs the unitests"""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    return 1

# run tests
if __name__ == '__main__':
    test()

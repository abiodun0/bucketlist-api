import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app, db


app = create_app(os.getenv('BUCKETLIST_LIST__API_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    """Discovers and runs unit tests"""
    # run the tests:
    import unittest
    tests = unittest.TestLoader().discover('tests')
    print tests
    unittest.TextTestRunner(verbosity=1).run(tests)


from app import models

if __name__ == '__main__':
	os.environ.update({'BUCKETLIST_LIST__API_CONFIG': 'development'})
	manager.run()
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=False, include='app/*')
    COV.start()

    
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db, models


#create the app from the pre-configured action given by the user
app = create_app(os.getenv('BUCKETLIST_LIST__API_CONFIG') or 'default')

#instantiate the app in a manager environmat
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'

        #restarts the script with the enviroment variable set
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()




if __name__ == '__main__':
	os.environ.update({'BUCKETLIST_LIST__API_CONFIG': 'development'})
	manager.run()
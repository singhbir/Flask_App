from models import Studentdata, authusers, db
import unittest
from run import app


class TestMyApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.app_context()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_deletentry(self):
        task = Studentdata(name='bir', teacher='Mr.singh')
        db.session.add(task)
        db.session.commit()
        deletentry(1)
        self.assertEqual(Studentdata.query.count(), 0)

    def test_updatentry(self):
        task = Studentdata(name='bir', teacher='Mr.singh')
        db.session.add(task)
        db.session.commit()
        self.app.get('/update/1')
        self.app.post('/update/1', content_type='multipart/form-data',
                                    data={'sname':'birvarinder',
                                          'tname':'Singh',
                                          })
        self.app.get('/update/1')
        p = db.engine.execute("select name from studentdata where teacher='Singh'")
        result = [row[0] for row in p]
        self.assertEqual(result[0], 'birvarinder')

    def test_hello_world(self):
        rv = self.app.get('/sdata')
        self.assertEqual(rv.status, '308 PERMANENT REDIRECT')

    def test_checkauth(self):
        task = authusers(email='q@gmail.com', password='123')
        db.session.add(task)
        db.session.commit()
        self.app.get('/mainlogin')
        r=self.app.post('/mainlogin', content_type='multipart/form-data',
                      data={'lemail': 'q@gmail.com',
                            'lpassword': '123',
                            })
        self.assertEqual(r.status, '302 FOUND')
import unittest
from fastapi.testclient import TestClient
from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers.get('content-type', ''))

    def test_create_project_and_list(self):
        response = self.client.post('/create_project', data={'name': 'unittest_project'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/list_projects')
        self.assertIn('unittest_project', response.json().get('projects', []))

    def test_create_chat_and_list(self):
        self.client.post('/create_project', data={'name': 'unittest_project2'})
        response = self.client.post('/create_chat', data={'project': 'unittest_project2', 'chat_name': 'chat1'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/list_chats', params={'project': 'unittest_project2'})
        self.assertIn('chat1', response.json().get('chats', []))

    def test_upload_image(self):
        img_bytes = b'\x89PNG\r\n\x1a\n' + b'0' * 100
        response = self.client.post('/upload_image', files={'file': ('test.png', img_bytes, 'image/png')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('base64', response.json())

if __name__ == '__main__':
    unittest.main()

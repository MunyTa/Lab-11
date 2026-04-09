import unittest
import json
import requests
import os
import subprocess
import time
import signal
import sys

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Запускаем сервер перед тестами"""
        os.environ['PORT'] = '8888'
        os.environ['DEBUG'] = 'false'
        
        if sys.platform == 'win32':
            cls.process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            cls.process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
        
        time.sleep(2)
    
    @classmethod
    def tearDownClass(cls):
        """Останавливаем сервер после тестов"""
        if sys.platform == 'win32':
            cls.process.terminate()
        else:
            os.killpg(os.getpgid(cls.process.pid), signal.SIGTERM)
        cls.process.wait()
    
    def test_health_endpoint(self):
        """Тест эндпоинта /health"""
        response = requests.get('http://localhost:8888/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})
    
    def test_root_endpoint(self):
        """Тест корневого эндпоинта /"""
        response = requests.get('http://localhost:8888/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")
    
    def test_404_not_found(self):
        """Тест несуществующего эндпоинта"""
        response = requests.get('http://localhost:8888/notfound')
        self.assertEqual(response.status_code, 404)
    
    def test_port_env_var(self):
        """Тест использования переменной PORT"""
        self.tearDownClass()
        
        os.environ['PORT'] = '8889'
        if sys.platform == 'win32':
            process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
        
        time.sleep(2)
        
        response = requests.get('http://localhost:8889/health')
        self.assertEqual(response.status_code, 200)
        
        if sys.platform == 'win32':
            process.terminate()
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait()
        
        self.setUpClass()

if __name__ == '__main__':
    unittest.main()
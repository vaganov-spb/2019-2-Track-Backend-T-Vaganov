import json
import codecs
from django.test import TestCase, Client
from django.test.client import RequestFactory
from unittest.mock import patch
from chats.views import attachment_save
# Create your tests here.


class GetChats(TestCase):
    def setUp(self):
        self.client = Client()

    def test_non_exist_chats(self):
        response = self.client.get('/chats/10/')
        self.assertEqual(response.status_code, 404)

    def test_exist_chats(self):
        response = self.client.get('/chats/1/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content[0]['chat_id'], 3)


class CreateChat(TestCase):
    def setUp(self):
        self.client = Client()

    def test_new_chat(self):
        response = self.client.post('/chats/1/newchat/', {'topic': 'test_chat'})
        content = json.loads(response.content)
        self.assertEqual(content['status'], 'Чат создан')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_topic_empty(self):
        response = self.client.post('/chats/1/newchat/', {'topic': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual((json.loads(response.content))['errors']['topic'][0], "Обязательное поле.")

    def test_incorrect_user(self):
        response = self.client.post('/chats/10/newchat/', {'topic': 'test_chat'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual((json.loads(response.content))['errors']['topic'][0], "No such user to create chat")


class ListOfMessages(TestCase):
    def setUp(self):
        self.client = Client()

    def test_correct(self):
        response = self.client.get('/users/1/messages/?chatId=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((json.loads(response.content))[0]['text'], "Сообщение 1")

    def test_incorrect_chat_id(self):
        response = self.client.get('/users/1/messages/?chatId=100')
        self.assertEqual(response.status_code, 404)

    def test_without_chat_id(self):
        response = self.client.get('/users/1/messages/')
        self.assertEqual(response.status_code, 400)


class CreateMessage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_correct_message(self):
        response = self.client.post('/chats/1/newmessage/', {'chatId': 2, 'content': 'sss'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), 'OK')

    def test_incorrect_info(self):
        response = self.client.post('/chats/1/newmessage/', {'chatId': 10, 'content': 'sss'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual((json.loads(response.content))['errors']['content'][0], 'Cant Find such chat member, check user id or chat id')


class ChatInfo(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('chats.views.returnedTrue')
    def test_get_chat_mock(self, mock_func):
        response = self.client.get('/chats/1/2/')
        self.assertTrue(mock_func.called)
        self.assertEqual(mock_func.call_count, 1)

    def test_get_correct_chat(self):
        response = self.client.get('/chats/1/2/')
        self.assertEqual(json.loads(response.content)['last message'], '111')

    def test_get_incorrect_chat(self):
        response = self.client.get('/chats/1/100/')
        self.assertEqual(response.status_code, 404)


class ReadMessageCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_correct_read(self):
        response = self.client.post('/chats/1/2/readmess/', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), 'OK')

    def test_incorrect_read(self):
        response = self.client.post('/chats/1/100/readmess/', {})
        self.assertEqual(response.status_code, 404)


class AttachmentSave(TestCase):
    def setUp(self):
        self.request = RequestFactory()

    @patch('storages.backends.s3boto3.S3Boto3Storage.save')
    def test_correct_save(self, mock_save):
        mock_save.return_value = '/Users/apple/Downloads/z-sol.pdf'
        with codecs.open('/Users/apple/Downloads/z-sol.pdf', 'r', encoding='utf-8', errors='ignore') as fl:
            request = self.request.post('/chats/attachment/', {'chat_id': 2, 'user_id': 1, 'file': fl})
        response = attachment_save(request)
        self.assertEqual(json.loads(response.content), {'status': 200})
        mock_save.assert_called_once()


class GetAttachment(TestCase):
    def setUp(self):
        self.client = Client()

    def test_correct(self):
        response = self.client.get('/chats/1/attachment/19')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("track_vaganov/media/2/5809612d0f89463bac39c2b" in json.loads(response.content))

    def test_incorrect_invalid_attach(self):
        response = self.client.get('/chats/1/attachment/109')
        self.assertEqual(json.loads(response.content), "No such doc")

    def test_incorrect_invalid_user(self):
        response = self.client.get('/chats/100/attachment/19')
        self.assertEqual(json.loads(response.content), "Not Allowed")



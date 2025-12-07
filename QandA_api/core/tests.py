# tests.py
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Question, Answer
from django.db import IntegrityError

class APITests(APITestCase):
    def setUp(self):
        # Создаём тестовые данные
        self.question_data = {'text': 'Test question'}
        self.answer_data = {'text': 'Test answer', 'question': 1, 'user_id': '12345678-1234-5678-9012-123456789012'}  # user_id как UUID
        # Создаём вопрос для тестов
        self.question = Question.objects.create(text='Existing question')

    def test_create_question(self):
        """Тест создания вопроса"""
        response = self.client.post('/api/questions/', self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)  # Один уже в setUp
        self.assertEqual(response.data['text'], self.question_data['text'])

    def test_create_question_empty_text(self):
        """1) Тест: при вводе пустого текста для вопроса (должен быть 400)"""
        response = self.client.post('/api/questions/', {'text': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверяем, что вопрос не создан
        self.assertEqual(Question.objects.count(), 1)

    def test_get_questions(self):
        """Тест получения списка вопросов"""
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_single_question(self):
        """Тест получения одного вопроса"""
        response = self.client.get(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.question.text)

    def test_update_question(self):
        """Тест обновления вопроса"""
        updated_data = {'text': 'Updated question'}
        response = self.client.put(f'/api/questions/{self.question.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, updated_data['text'])

    def test_delete_question(self):
        """Тест удаления вопроса"""
        response = self.client.delete(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

    def test_delete_question_cascades_answers(self):
        """3) Тест: удаляются ли ответы при удалении вопроса (да, CASCADE)"""
        answer = Answer.objects.create(text='Test answer', question=self.question, user_id='12345678-1234-5678-9012-123456789012')
        self.assertEqual(Answer.objects.count(), 1)
        # Удаляем вопрос
        self.client.delete(f'/api/questions/{self.question.id}/')
        # Проверяем, что ответ тоже удалён
        self.assertEqual(Answer.objects.count(), 0)

    def test_create_answer(self):
        """Тест создания ответа"""
        self.answer_data['question'] = self.question.id
        response = self.client.post('/api/answers/', self.answer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(response.data['text'], self.answer_data['text'])

    def test_create_answer_empty_text(self):
        """2) Тест: при вводе пустого текста для ответа (должен быть 400)"""
        data = {'text': '', 'question': self.question.id, 'user_id': '12345678-1234-5678-9012-123456789012'}
        response = self.client.post('/api/answers/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Answer.objects.count(), 0)

    def test_create_answer_to_nonexistent_question(self):
        """4) Тест: можно ли создать ответ к несуществующему вопросу (должен быть IntegrityError или 400)"""
        data = {'text': 'Test answer', 'question': 999, 'user_id': '12345678-1234-5678-9012-123456789012'}  # Несуществующий question_id
        response = self.client.post('/api/answers/', data)
        # FK должен вызвать IntegrityError, что приведёт к 500 или 400 в DRF
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR])
        self.assertEqual(Answer.objects.count(), 0)

    def test_get_answers(self):
        """Тест получения списка ответов"""
        Answer.objects.create(text='Existing answer', question=self.question, user_id='12345678-1234-5678-9012-123456789012')
        response = self.client.get('/api/answers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_single_answer(self):
        """Тест получения одного ответа"""
        answer = Answer.objects.create(text='Existing answer', question=self.question, user_id='12345678-1234-5678-9012-123456789012')
        response = self.client.get(f'/api/answers/{answer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], answer.text)

    def test_update_answer(self):
        """Тест обновления ответа"""
        answer = Answer.objects.create(text='Existing answer', question=self.question, user_id='12345678-1234-5678-9012-123456789012')
        updated_data = {'text': 'Updated answer', 'question': self.question.id, 'user_id': '12345678-1234-5678-9012-123456789012'}
        response = self.client.put(f'/api/answers/{answer.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer.refresh_from_db()
        self.assertEqual(answer.text, updated_data['text'])

    def test_delete_answer(self):
        """Тест удаления ответа"""
        answer = Answer.objects.create(text='Existing answer', question=self.question, user_id='12345678-1234-5678-9012-123456789012')
        response = self.client.delete(f'/api/answers/{answer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.count(), 0)

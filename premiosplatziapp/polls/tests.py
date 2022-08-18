from django.utils import timezone
from django.test import TestCase
from .models import Question

import datetime


# Se testean modelos y vistas
class QuestionModelTests(TestCase):

    def setUp(self) -> None:
        self.question = Question(question_text="Quien es el mejor Course Director de Platzi?")

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns false for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recnetly(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns false for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=-15)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recnetly(), False)

    def test_was_published_recently_present_questions(self):
        """was_published_recently returns true for questions whose pub_date is in the present"""
        time = timezone.now() - datetime.timedelta(hours=22)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recnetly(), True)

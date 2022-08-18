from django.urls.base import reverse
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
        
    

class QuestionIndexViewTets(TestCase):

    def setUp(self) -> None:
        self.question = Question(question_text="Pregunta Generica ??")
        

    # Test para verificar que pasa cuando no hay preguntas    
    def test_no_questions(self):
        """If no question exists, an apropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_with_future_pub_date(self):
        """Questions with pub_date greater than actual shouldn't be displayed """
        time = timezone.now() + datetime.timedelta(minutes=1)
        self.question.pub_date = time
        self.question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.question,response.context["latest_question_list"])
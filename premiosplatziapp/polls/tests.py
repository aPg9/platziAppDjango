from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase
from .models import Question


import datetime


def create_question(question_text, days):
    """Create a question with the given "question_text", and publish the given number of days offset to now (negative for questions published in the past, positive for questions that have yet to be published"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
        

# Se testean modelos y vistas
class QuestionModelTests(TestCase):

    def setUp(self) -> None:
        self.question = Question(question_text="pregunta generica??")

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
    

class QuestionIndexViewTests(TestCase):
    # Test para verificar que pasa cuando no hay preguntas    
    def test_no_questions(self):
        """If no question exists, an apropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_with_future_pub_date(self):
        """Questions with pub_date greater than actual date shouldn't be displayed """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")        
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question_pub_date(self):
        """Questions with pub_date in the past are diplayed on index page"""
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """Even if both past and future question exist, only past question are displayed"""
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Past question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions"""
        past_question1 = create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])

    def test_two_future_questions(self):
        future_question1 = create_question(question_text="Future question 1", days=30)
        future_question2 = create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
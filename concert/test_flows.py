from unittest.mock import patch, Mock
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Concert

class ApplicationFlowTests(TestCase):
    def test_signup_hashes_password_and_logs_in(self):
        r=self.client.post('/signup/', {'username':'listener','password':'TestOnly-284!_Q'})
        self.assertEqual(r.status_code,302)
        u=User.objects.get(username='listener')
        self.assertTrue(u.check_password('TestOnly-284!_Q'))
        self.assertNotEqual(u.password,'TestOnly-284!_Q')
        self.assertEqual(self.client.get('/concerts/').status_code,200)

    def test_attendance_requires_authentication_and_persists(self):
        self.assertEqual(self.client.get('/concerts/').status_code,302)
        u=User.objects.create_user(username='guest',password='TestOnly-284!_Q')
        c=Concert.objects.create(concert_name='Local test concert',city='Astana')
        self.client.force_login(u)
        self.client.post('/concert_attendee/', {'concert_id':c.pk,'attendee_choice':'Attending'})
        self.assertEqual(c.attendee.get(user=u).attending,'Attending')

    @patch('concert.views.req.get')
    def test_service_data_is_rendered(self,get):
        get.return_value=Mock(json=lambda:[{'id':1,'title':'Test song','lyrics':'Test lyrics'}])
        r=self.client.get('/songs/')
        self.assertContains(r,'Test lyrics')
        get.return_value=Mock(json=lambda:[{'id':1,'pic_url':'https://example.com/a.png','event_city':'Astana'}])
        self.assertContains(self.client.get('/photos/'),'Astana')

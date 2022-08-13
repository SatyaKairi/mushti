from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

# Create your tests here.
class TestProject(TestCase):
    
    def setUp(self):
        
        self.u1 = User.objects.create(username = "bhanu", email="")
        self.u2 = User.objects.create(username = 'satya', email='')
        self.u3 = User.objects.create(username = 'satya1', email='')
        self.p1 = Project.objects.create(
            name = "P1", description = "P1 Description", budget =1000.00, user = self.u1
        )
        self.p2 = Project.objects.create(
            name = "P2", description = "P2 Description", budget =2000.00, user = self.u1
        )
        # p1 contrib
        self.c1 = ProjectContribution.objects.create(project = self.p1, amount =100, contributor = self.u2)
        self.c2 = ProjectContribution.objects.create(project = self.p1, amount =200, contributor = self.u2)
        self.c3 = ProjectContribution.objects.create(project = self.p1, amount =300, contributor = self.u3)
        # p2 contrib
        self.d1 = ProjectContribution.objects.create(project = self.p2, amount =100, contributor = self.u2)

    def testFundedAmount(self):
        
        funded = self.p1.get_funded_amount()
        self.assertEqual(funded,600)
        funded = self.p2.get_funded_amount()
        self.assertEqual(funded,100)
        
    def testActiveContributions(self):
        self.c1.is_active = False
        self.c1.save()
        rs = self.p1.get_active_contributions()
        self.assertEqual(rs.count(),3)

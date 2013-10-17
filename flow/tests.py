"""
Unit tests for neighbor application.

Author: Quentin Loos <contact@quentinloos.be>
"""

from django.test import TestCase
from django.utils import timezone

from models import Flow, Match, Then


class FlowTest(TestCase):

    def setUp(self):
        self.flow         = Flow()
        self.name         = "Test"
        self.description  = "A test flow"

        self.expires      = timezone.now()

        self.match        = Match()
        self.then         = Then()
        self.flow.save()

"""
Unit tests for neighbor application.

Author: Quentin Loos <contact@quentinloos.be>
"""

from django.test import TestCase

from models import Neighbor


class NeighborTest(TestCase):

    def setUp(self):
        self.neighbor = Neighbor()
        self.neighbor.name = 'test'
        self.neighbor.description = 'description test'
        self.neighbor.router_id = '10.0.0.1'
        self.neighbor.local_address = '10.0.0.1'
        self.neighbor.peer_address = '10.0.0.2'
        self.neighbor.local_as = 65000
        self.neighbor.peer_as = 65100
        self.neighbor.enable = True
        self.neighbor.save()

    def test_enable(self):
        """
        Test if the enable field and method connect and disconnect are correct.
        """

        self.assertEqual(self.neighbor.enable_changed(), False)
        self.neighbor.enable = True
        self.assertEqual(self.neighbor.enable_changed(), False)
        self.neighbor.enable = False
        self.assertEqual(self.neighbor.enable_changed(), True)

        self.neighbor.disconnect()
        self.assertEqual(self.neighbor.enable, False)
        self.neighbor.disconnect()
        self.assertEqual(self.neighbor.enable, False)

        self.neighbor.save()
        self.neighbor.connect()
        self.assertEqual(self.neighbor.enable_changed(), True)

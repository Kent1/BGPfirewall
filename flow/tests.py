"""
Unit tests for neighbor application.

Author: Quentin Loos <contact@quentinloos.be>
"""
import datetime

from django.test import TestCase
from django.utils import timezone

from flow.models import Flow
from flow import tasks


class FlowTest(TestCase):

    def setUp(self):
        self.flow             = Flow()
        self.flow.name = "Test"
        self.flow.description = "A test flow"

        #self.flow.expires      = timezone.now() + datetime.timedelta(days=1)

        self.flow.save()

        self.flow.destination = '1.2.3.4/32'
        self.flow.source = '4.3.2.1/23'

        self.flow.protocol_set.create(protocol=12)
        self.flow.protocol_set.create(protocol=123)

        self.flow.port_set.create(port_number=23)
        self.flow.port_set.create(port_number=234, direction="source-port")

        self.flow.packetlength_set.create(packet_length=23)
        self.flow.packetlength_set.create(packet_length='>432')

        self.flow.dscp_set.create(dscp='<2')

        self.flow.icmp_set.create(icmp_type=3, icmp_code=0)
        self.flow.icmp_set.create(icmp_type=1)

        self.flow.tcpflag_set.create(tcp_flag=2)

        self.flow.fragment_set.create(fragment=8)

        self.flow.active = True
        self.flow.save()

    def test_init(self):
        self.assertEqual(self.flow.status, 5) # INACTIVE

    def test_has_expired(self):
        self.assertFalse(self.flow.has_expired())
        self.flow.expires = timezone.now() - datetime.timedelta(hours=1)
        self.assertTrue(self.flow.has_expired())

    def test_match(self):
        match = self.flow.match()
        self.assertEqual(match['source'], '4.3.2.1/23')
        self.assertEqual(match['destination'], '1.2.3.4/32')
        self.assertItemsEqual(match['protocol'], [12, 123])
        self.assertItemsEqual(match['port'], ['23'])
        self.assertItemsEqual(match['source-port'], ['234'])
        self.assertItemsEqual(match['destination-port'], [])
        self.assertItemsEqual(match['packet-length'], ['23', '>432'])
        self.assertItemsEqual(match['dscp'], ['<2'])
        self.assertItemsEqual(match['icmp-type'], [1, 3])
        self.assertItemsEqual(match['icmp-code'], [0])
        self.assertItemsEqual(match['tcp-flags'], [2])
        self.assertItemsEqual(match['fragment'], [8])

    def test_then(self):
        then = self.flow.then()
        self.assertEquals(then, 'accept')


class TaskTest(TestCase):

    def setUp(self):
        self.flow = Flow()

        self.flow.name = "Test"
        self.flow.description = "A test flow"

        #self.flow.expires      = timezone.now() + datetime.timedelta(days=1)

        self.flow.save()

        self.flow.destination = '1.2.3.4/32'
        self.flow.source = '4.3.2.1/23'

        self.flow.protocol_set.create(protocol=12)
        self.flow.protocol_set.create(protocol=123)

        self.flow.port_set.create(port_number=23)
        self.flow.port_set.create(port_number=234, direction="source-port")

        self.flow.packetlength_set.create(packet_length=23)
        self.flow.packetlength_set.create(packet_length='>432')

        self.flow.dscp_set.create(dscp='<2')

        self.flow.icmp_set.create(icmp_type=3, icmp_code=0)
        self.flow.icmp_set.create(icmp_type=1)

        self.flow.tcpflag_set.create(tcp_flag=2)

        self.flow.fragment_set.create(fragment=8)

        self.flow.active = True
        self.flow.save()

    def test_announce(self):
        task = tasks.announce.delay(self.flow)
        self.assertTrue(task.successful())

    def test_withdraw(self):
        task = tasks.withdraw.delay(self.flow, self.flow.match, self.flow.then)
        self.assertTrue(task.successful())

    def test_delete(self):
        task = tasks.withdraw.delay(self.flow, self.flow.match, self.flow.then)
        self.assertTrue(task.successful())

    def test_expire(self):
        task = tasks.withdraw.delay(self.flow, self.flow.match, self.flow.then)
        self.assertTrue(task.successful())

from django.core import management
from django.test import TestCase


class CommandTestCase(TestCase):
    """
    Test cases for django-ph-geography custom commands
    """

    def run_command_phgeofixtures(self):
        """Run custom manage.py command 'phgeofixtures'"""
        management.call_command('phgeofixtures', verbosity=0)
        return True

    def test_command_phgeofixtures(self):
        self.assertTrue(self.run_command_phgeofixtures())

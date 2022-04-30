# -*- coding: utf-8 -*-
"""Common development tasks for setup.py to use."""

import re
import subprocess
import sys

from setuptools import Command
from setuptools.command.test import test as TestCommand


class BaseCommand(Command, object):
    """The base command for project tasks."""

    user_options = []

    default_cmd_options = ("verbose", "quiet", "dry_run")

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.verbose = False

    def initialize_options(self):
        """Override the distutils abstract method."""
        pass

    def finalize_options(self):
        """Override the distutils abstract method."""
        # Distutils uses incrementing integers for verbosity.
        self.verbose = bool(self.verbose)

    def call_and_exit(self, cmd, shell=True):
        """Run the *cmd* and exit with the proper exit code."""
        sys.exit(subprocess.call(cmd, shell=shell))

    def call_in_sequence(self, cmds, shell=True):
        """Run multiple commmands in a row, exiting if one fails."""
        for cmd in cmds:
            if subprocess.call(cmd, shell=shell) == 1:
                sys.exit(1)

    def apply_options(self, cmd, options=()):
        """Apply command-line options."""
        for option in self.default_cmd_options + options:
            cmd = self.apply_option(cmd, option, active=getattr(self, option, False))
        return cmd

    def apply_option(self, cmd, option, active=True):
        """Apply a command-line option."""
        return re.sub(
            r"{{{}\:(?P<option>[^}}]*)}}".format(option),
            r"\g<option>" if active else "",
            cmd,
        )


class lint(BaseCommand):
    description = "check code using black (and fix violations)"

    user_options = [("fix", "f", "fix the violations in place")]

    def initialize_options(self):
        """Set the default options."""
        self.fix = False

    def finalize_options(self):
        pass

    def run(self):
        cmd = "black"
        if not self.fix:
            cmd += " --check"
        cmd += " ."
        sys.exit(subprocess.call(cmd, shell=True))


class test(TestCommand):

    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        unit_test_errno = subprocess.call(
            "pytest tests " + self.pytest_args, shell=True
        )
        # cli_errno = subprocess.call('behave test/features', shell=True)
        # sys.exit(unit_test_errno or cli_errno)
        sys.exit(unit_test_errno)

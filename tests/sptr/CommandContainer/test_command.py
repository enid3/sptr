import unittest

from sptr.commands.command import CommandContainer, Command


class TestCommandContainer(unittest.TestCase):
    def test_get_command_throws_ValueError_when_result_ambiguous(self):
        c = CommandContainer()
        c.commands = {'cmd1': Command('cmd1'), 'cmd2': Command('cmd2')}
        self.assertRaises(ValueError, c.get_command, 'cmd', True)


if __name__ == '__main__':
    unittest.main()

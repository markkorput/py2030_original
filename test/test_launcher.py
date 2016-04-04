import test_helper
from launcher import Launcher

import unittest, os, time

import threading

class TestLauncher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # this happens only once for the whole TestLauncher test-suite
        cls.launcher = Launcher()
        cls.launcher.setup()

    def setUp(self):
        # this happens before each test
        self.launcher = self.__class__.launcher

    def test_run_and_stop(self):
        # create separate thread to run launcher's main loop
        thread = threading.Thread(target=self._threadMain)
        # verify launcher isn't running yet
        self.assertFalse(self.launcher.running)
        # start thread
        thread.start()
        # verify that the thread is alive
        self.assertTrue(thread.isAlive())
        # verify that the launcher is running
        self.assertTrue(self.launcher.running)
        # tell launcher to stop
        self.launcher.stop()
        # give the thread a ms to finish
        time.sleep(0.001)
        # verify launcher is not running anymore
        self.assertFalse(self.launcher.running)
        # verify thread has ended as well
        self.assertFalse(thread.isAlive())
        del thread

    def _threadMain(self):
        # run the launcher's main loop (this will loop forever until requested to stop)
        self.launcher.run()
        return

    def test_osc_broadcast(self):
        # setup
        self.sent_messages = []
        self.launcher.controller.osc_output.messageEvent += self._onOscMessage

        # before
        self.assertEqual(len(self.sent_messages), 0)

        # do broadcasts
        self.launcher.controller.interval_broadcast.broadcast()
        self.launcher.controller.interface.broadcasts.create({'data': '123-test-check'})
        self.launcher.controller.interface.broadcasts.create()

        # after
        self.assertEqual(len(self.sent_messages), 3)
        self.assertEqual(self.sent_messages[0][0], 'TODO: controller info JSON')
        self.assertEqual(self.sent_messages[1][0], '123-test-check')
        self.assertEqual(len(self.sent_messages[2]), 0)

    def _onOscMessage(self, message, osc_output):
        self.sent_messages.append(message)


if __name__ == '__main__':
    unittest.main()

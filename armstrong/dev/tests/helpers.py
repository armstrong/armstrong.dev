import copy


class RestoreSignalReceivers(object):
    """
    Mixin for making sure that signal receivers are restored after
    test methods.

    Mix this class into your TestCase and add an iterable property
    called ``watched_signals`` that has references to each signal you
    want to restore after the test run.

    One final note, make sure your TestCase's ``setUp`` and ``tearDown``
    include a call to ``super`` so these get called.
    """
    def setUp(self):
        if not hasattr(self, "watched_signals"):
            return
        self._receivers_to_restore = {}
        for signal in self.watched_signals:
            self._receivers_to_restore[id(signal)] = copy.deepcopy(
                    signal.receivers)

    def tearDown(self):
        if not hasattr(self, "watched_signals"):
            return

        for signal in self.watched_signals:
            if not id(signal) in self._receivers_to_restore:
                continue
            signal.receivers = self._receivers_to_restore[id(signal)]

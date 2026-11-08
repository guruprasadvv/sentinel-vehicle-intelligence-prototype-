"""Known gaps found in experiment 5, recorded as expected failures. Nothing is fixed here.

Each test states the behaviour we want and currently fails. Remove the
`expectedFailure` marker only together with the fix. Plates are SYNTHETIC and
only masked forms are asserted on or written out.
"""
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest

from ctc_fixtures import reader_with
from sentinel_edge.passages import PassageOutcome
from sentinel_edge.plate_options import PlateOptions
from sentinel_edge.result_state import classify
from sentinel_edge.shared_delivery import PARTIAL_DUPLICATE_WINDOW_MS, SharedDelivery

KEY = 'test-hmac-key'
PLATE = 'MH49BE5557'  # synthetic, never a real plate


def config(directory):
    return SimpleNamespace(db_path=Path(directory) / 'outbox.sqlite3', central_api_url='http://127.0.0.1:9',
                           edge_api_key='edge-key', edge_id='edge-1', hmac_key=KEY)


def weak(position, rival):
    spec = list(PLATE)
    spec[position] = (PLATE[position], .45, rival)
    return spec


def partial_at(passage_id, first_pts, last_pts):
    result = classify(reader_with([weak(5, 'F'), weak(5, 'F'), list('MH49BF5557')]))
    return PassageOutcome(passage_id, (passage_id,), 2, first_pts, last_pts, result, 'expired',
                          first_box=(0, 0, 100, 60), last_box=(10, 0, 110, 60))


def confirmed_at(passage_id, first_pts, last_pts):
    result = classify(reader_with([list(PLATE)] * 3))
    return PassageOutcome(passage_id, (passage_id,), 3, first_pts, last_pts, result, 'expired',
                          confirmed_plate=PLATE, first_box=(0, 0, 100, 60), last_box=(10, 0, 110, 60))


class Experiment5Findings(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.options = PlateOptions()

    def delivery(self, clock=None):
        kwargs = {'clock': clock} if clock else {}
        return SharedDelivery(config(self.directory.name), 'general', options=self.options, **kwargs)

    @unittest.expectedFailure
    def test_live_sighting_is_not_repeated_after_restart(self):
        """The live 60 s repeat window is in memory only, so a restart re-sends the same plate."""
        candidate = SimpleNamespace(plate=PLATE, score=.95)
        first = self.delivery(clock=lambda: 100.0)
        self.assertTrue(first.accept('cam01', '3', candidate, 1000))
        restarted = self.delivery(clock=lambda: 110.0)  # 10 s later, same camera and identifier
        self.assertFalse(restarted.accept('cam01', '4', candidate, 11000),
                         'same identifier on the same camera inside 60 s was sent again after restart')

    @unittest.expectedFailure
    def test_suppressed_result_leaves_a_durable_trace(self):
        """A suppressed passage is only counted in memory; nothing survives a restart."""
        delivery = self.delivery()
        self.assertIsNotNone(delivery.finalized('cam01', confirmed_at('a', 0, 1000)))
        self.assertIsNone(delivery.finalized('cam01', partial_at('b', 2000, 3000)))
        self.assertEqual(delivery.result_metrics['suppressed_compatible_with_recent_reading'], 1)
        del delivery
        connection = sqlite3.connect(Path(self.directory.name) / 'outbox.sqlite3')
        try:
            dump = '\n'.join(connection.iterdump()).lower()
        finally:
            connection.close()
        self.assertIn('suppressed', dump, 'no durable record that a passage was suppressed, or why')

    @unittest.expectedFailure
    def test_suppressed_partial_does_not_extend_the_window(self):
        """A suppressed partial is appended to recent_results, so it renews the 10 s window."""
        delivery = self.delivery()
        self.assertIsNotNone(delivery.finalized('cam01', confirmed_at('a', 0, 1000)))
        inside = 1000 + PARTIAL_DUPLICATE_WINDOW_MS - 1000   # compatible, inside the window: suppressed
        self.assertIsNone(delivery.finalized('cam01', partial_at('b', inside, inside + 500)))
        # Beyond 10 s from the *confirmed* reading, but within 10 s of the suppressed partial.
        later = 1000 + PARTIAL_DUPLICATE_WINDOW_MS + 2000
        self.assertIsNotNone(delivery.finalized('cam01', partial_at('c', later, later + 500)),
                             'window was renewed by a passage that was itself suppressed')


if __name__ == '__main__':
    unittest.main()

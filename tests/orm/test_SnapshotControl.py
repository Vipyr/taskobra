from .ORMTestCase import ORMTestCase
from taskobra.orm import SnapshotControl


class TestSnapshotControl(ORMTestCase):
    def test_creation(self):
        snapshot_control = SnapshotControl()
        self.assertEqual(snapshot_control.pruning_delay, SnapshotControl.pruning_delay.default.arg)
        self.assertEqual(snapshot_control.max_prune_time_slice, SnapshotControl.max_prune_time_slice.default.arg)
        self.assertEqual(snapshot_control.default_sample_base, SnapshotControl.default_sample_base.default.arg)
        self.assertEqual(snapshot_control.default_sample_rate, SnapshotControl.default_sample_rate.default.arg)

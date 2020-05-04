from ..ORMTestCase import ORMTestCase
from taskobra.orm import get_engine, get_session, Snapshot, System


class TestSystemSnapshot(ORMTestCase):
    def test_SystemSnapshot_creation(self):
        system = System(
            snapshots=[
                Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 53)),
                Snapshot(timestamp=datetime(2020, 3, 9, 9, 53, 52)),
            ]
        )

        [self.assertIs(system, snapshot.system) for snapshot in system.snapshots]

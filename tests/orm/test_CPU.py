from .ORMTestCase import ORMTestCase
from sqlalchemy import create_engine
from taskobra.orm import get_engine, get_session, CPU, GPU, System


class TestCPU(ORMTestCase):
    def test_Polymorphism(self):
        # Put some data into the db
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            cpu = CPU(
                manufacturer="AMD",
                model="Ryzen 3800X",
                isa="x86-64",
                tdp=65,
                core_count=12,
                threads_per_core=2,
                minimum_frequency=3.0,
                maximum_frequency=4.2,
            )
            session.add(cpu)
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            cpus = session.query(CPU)
            cpu = cpus[0]
            self.assertEqual(cpu.manufacturer, "AMD")
            self.assertEqual(cpu.model, "Ryzen 3800X")
            self.assertEqual(cpu.isa, "x86-64")
            self.assertEqual(cpu.tdp, 65)
            self.assertEqual(cpu.core_count, 12)
            self.assertEqual(cpu.threads_per_core, 2)
            self.assertEqual(cpu.minimum_frequency, 3.0)
            self.assertEqual(cpu.maximum_frequency, 4.2)

from .ORMTestCase import ORMTestCase
from sqlalchemy import create_engine
from taskobra.orm import get_engine, get_session, CPU, GPU, Memory, System, SystemComponent


class TestCPU(ORMTestCase):
    def test_Polymorphism(self):
        # Put some data into the db
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            cpu = CPU(
                manufacturer="AMD",
                model="Ryzen 3800X",
                isa="x86-64",
                tdp=105,
                core_count=8,
                threads_per_core=2,
                minimum_frequency=3.9,
                maximum_frequency=4.5,
            )
            gpu = GPU(
                manufacturer="NVIDIA",
                model="1070",
                architecture="CUDA",
                tdp=105,
                core_count=1920,
                memory=8.0,
            )
            memory = Memory(
                manufacturer="G-Skill",
                model="Trident",
                capacity=16.0,
                frequency=3600,
                cas_latency=16,
                t_rcd=19,
                t_rp=19,
                t_ras=39,
            )
            system = System(name="Some System")
            system.add_component(cpu)
            system.add_component(gpu)
            system.add_component(memory)
            system.add_component(memory)
            session.add(system)
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            systems = session.query(System)
            self.assertEqual(len(list(systems)), 1)
            system = systems[0]
            cpu = session.query(CPU).first()
            gpu = session.query(GPU).first()
            memory = session.query(Memory).first()
            # Check that our system object is composed correctly
            self.assertEqual(system.name, "Some System")
            self.assertEqual(len(list(system.components)), 4)
            self.assertIn(cpu, system.components)
            self.assertIn(gpu, system.components)
            self.assertEqual(list(system.components).count(memory), 2)

from .ORMTestCase import ORMTestCase
from taskobra.orm import get_engine, get_session, ORMBase
from taskobra.orm import Component, Storage, System, CPU, GPU, Memory, OperatingSystem


class TestSystem(ORMTestCase):
    def test_add_component(self):
        # Put some data into the db
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            cpu = CPU(
                manufacturer="AMD",
                model="Ryzen 3800X",
                isa="x86-64",
                tdp=105,
                core_count=8,
                threads_per_core=2,
                nominal_frequency=3.9,
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
                standard="DDR4",
                capacity=16.0,
                frequency=3600,
                cas_latency=16,
                t_rcd=19,
                t_rp=19,
                t_ras=39,
            )
            storage = Storage(
                manufacturer="Sabrent",
                model="Rocket",
                standard="NVMe PCIe 4.0",
                capacity=500.0,
                max_read=5000,
                max_write=2500,
            )
            os = OperatingSystem(
                developer="Microsoft",
                name="Windows 10",
            )
            system = System(name="Some System")
            system.add_component(cpu)
            system.add_component(gpu)
            system.add_component(memory)
            system.add_component(memory)
            system.add_component(storage)
            system.add_component(os)
            session.add(system)
        with get_session(bind=get_engine("sqlite:///:memory:")) as session:
            systems = session.query(System)
            self.assertEqual(len(list(systems)), 1)
            system = systems[0]
            cpu = session.query(CPU).first()
            gpu = session.query(GPU).first()
            memory = session.query(Memory).first()
            storage = session.query(Storage).first()
            os = session.query(OperatingSystem).first()
            # Check that our system object is composed correctly
            self.assertEqual(system.name, "Some System")
            self.assertEqual(len(list(system.components)), 6)
            self.assertIn((1, cpu), system.components)
            self.assertIn((1, gpu), system.components)
            self.assertIn((2, memory), system.components)
            self.assertIn((1, storage), system.components)
            self.assertIn((1, os), system.components)

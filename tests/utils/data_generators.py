from taskobra.orm import Component, Storage, System, CPU, GPU, Memory, OperatingSystem

def fake_systems_generator(max_systems=None):
    count = 0
    while not max_systems or count < max_systems:
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
        system = System(name=f"System {count}")
        system.add_component(cpu)
        system.add_component(gpu)
        system.add_component(memory)
        system.add_component(memory)
        system.add_component(storage)
        system.add_component(os)
        yield system
        count += 1

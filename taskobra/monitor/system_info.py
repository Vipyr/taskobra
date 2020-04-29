from taskobra.orm import *
import platform
import cpuinfo
import subprocess


def create_system(args, database_engine):
    system = System(name=platform.node())
    cpu_info = cpuinfo.get_cpu_info()

    system.add_component(OperatingSystem(
        name=platform.system(),
        version=platform.platform(),
    ))

    system.add_component(CPU(
        manufacturer=cpu_info.get('vendor_id', ''),
        model=cpu_info.get('brand', ''),
        isa=cpu_info.get('arch', ''),
        core_count=cpu_info.get('count', 1),
        threads_per_core=1,
        nominal_frequency=(cpu_info.get('hz_actual_raw')[0] / 1000000000),
    ))

    with get_session(bind=database_engine) as session:
        current_system = session.query(System).filter(
            System.name == platform.node(),
        ).first()
        if current_system is None:
            session.add(system)
            session.commit()
        
    #gpu = GPU(
    #    manufacturer="NVIDIA",
    #    model="1070",
    #    architecture="CUDA",
    #    tdp=105,
    #    core_count=1920,
    #    memory=8.0,
    #)
    #memory = Memory(
    #    manufacturer="G-Skill",
    #    model="Trident",
    #    standard="DDR4",
    #    capacity=16.0,
    #    frequency=3600,
    #    cas_latency=16,
    #    t_rcd=19,
    #    t_rp=19,
    #    t_ras=39,
    #)
    #storage = Storage(
    #    manufacturer="Sabrent",
    #    model="Rocket",
    #    standard="NVMe PCIe 4.0",
    #    capacity=500.0,
    #    max_read=5000,
    #    max_write=2500,
    #)
    #system.add_component(gpu)
    #system.add_component(memory)
    #system.add_component(memory)
    #system.add_component(storage)

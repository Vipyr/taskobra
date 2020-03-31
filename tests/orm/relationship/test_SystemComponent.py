from ..ORMTestCase import ORMTestCase
from taskobra.orm import get_engine, get_session, Component, System, SystemComponent


class TestSystemComponent(ORMTestCase):
    def test_SystemComponent_user_property(self):
        system = System(name="Fred's Computer")
        component = Component()
        system_component = SystemComponent(system=system)
        system_component.component = component
        self.assertIn(system_component, component.system_components)
        self.assertIn(system, component.systems)

    def test_SystemComponent_system_property(self):
        system = System(name="Fred's Computer")
        component = Component()
        system_component = SystemComponent(component=component)
        system_component.system = system
        self.assertIn(system_component, system.system_components)
        self.assertIn((1, component), system.components)

    def test_SystemComponent_creation(self):
        with self.subTest("No Arguments"):
            system_component = SystemComponent()
            self.assertEqual(system_component.count, 1)
            self.assertIsNone(system_component.component)
            self.assertIsNone(system_component.system)
        with self.subTest("Component Only"):
            component = Component()
            system_component = SystemComponent(component=component)
            self.assertIs(system_component.component, component)
            self.assertIsNone(system_component.system)
        with self.subTest("System Only"):
            system = System(name="Fred's Computer")
            system_component = SystemComponent(system=system)
            self.assertIsNone(system_component.component)
            self.assertIs(system_component.system, system)
        with self.subTest("All"):
            component = Component()
            system = System(name="Fred's Computer")
            system_component = SystemComponent(system=system, component=component)
            self.assertIs(system_component.component, component)
            self.assertIs(system_component.system, system)
            self.assertIn(system_component, component.system_components)
            self.assertIn(system, component.systems)
            self.assertIn(system_component, system.system_components)
            self.assertIn((1, component), system.components)

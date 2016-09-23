import enum

from super_state_machine import extras, machines


class Lock(machines.StateMachine):

    class States(enum.Enum):

        OPEN = 'open'
        LOCKED = 'locked'

    class Meta:
        allow_empty = False
        initial_state = 'open'
        named_transitions = {
            ('lock', 'locked'),
            ('open', 'open'),
        }


def test_property_machine():

    class Door(object):

        lock1 = extras.PropertyMachine(Lock)
        lock2 = extras.PropertyMachine(Lock)

    door = Door()
    assert door.lock1 == 'open'
    assert door.lock2 == 'open'
    door.lock1.lock()
    assert door.lock1 == 'locked'
    assert door.lock2 == 'open'
    door.lock2.state_machine.lock()
    assert door.lock1 == 'locked'
    assert door.lock2 == 'locked'
    door.lock1.open()
    door.lock2.open()
    assert door.lock1 == 'open'
    assert door.lock2 == 'open'


def test_can_be_property_of_non_hashable_objects():

    class Door(object):

        lock1 = extras.PropertyMachine(Lock)
        lock2 = extras.PropertyMachine(Lock)

        def __hash__(self):
            raise RuntimeError('You shall not pass!')

    door = Door()
    assert door.lock1 == 'open'
    assert door.lock2 == 'open'
    door.lock1.lock()

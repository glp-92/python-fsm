'''
    pip install pylint
    pylint FSM.py
'''

class StateDeclarationError(Exception):
    pass


class TransitionDeclarationError(Exception):
    pass



class FSM:

    """
    Represents a Finite State Machine (FSM).

    This class allows for the definition and control of states and transitions in an FSM.

    Attributes:
        states (dict): A dictionary that stores the states and their transitions.
        current_state (int): The current state of the FSM.

    Methods:
        add_state(state_id: int, callback: callable) -> None:
            Adds a new state to the FSM.

        del_state(state_id: int) -> None:
            Deletes a state from the FSM.

        add_transition(origin_state: int, destiny_state: int, callback: callable) -> None:
            Adds a transition between two states in the FSM.

        start() -> None:
            Starts the execution of the FSM.

        send(value_to_send) -> None:
            Sends a value to the FSM for processing.

        task() -> None:
            The generator function that represents the FSM's task.

    Example Usage:
        fsm = FSM()
        fsm.add_state(0, lambda: print('state1'))
        fsm.add_state(1, lambda: print('state2'))
        fsm.add_transition(0, 1, condition_func)
        fsm.start()
        fsm.send(value)
    """

    def __init__(self):
        """
        states = {
            0: {
                'func': callback,
                'transitions': [
                    {
                        'destiny_state': 1,
                        'condition': cond1_callback
                    },
                    {
                        'destiny_state': 2,
                        'condition': cond2_callback
                    }...
                ]
            }...
        }
        """
        self.states = {}
        self.current_state = 0
        self.task_gen = self.task()

    def add_state(self, state_id: int, callback: callable):
        """
        Add a state to the finite state machine.

        Args:
            state_id (int): The ID of the state.
            callback (callable): The function to be executed for the state.

        Raises:
            StateDeclarationError: If the state ID is not an integer or callback is not callable.
        """
        if not isinstance(state_id, int) or not callable(callback):
            raise StateDeclarationError('Error on state declaration: state_id -> int, callback -> func')
           
        if state_id in self.states:
            raise StateDeclarationError(f'State {state_id} already exists!')

        self.states[state_id] = {
            'func': callback,
            'transitions': []
        }

    def del_state(self, state_id: int):
        """
        Delete a state from the finite state machine.

        Args:
            state_id (int): The ID of the state.
        """
        del self.states[state_id]

    def add_transition(self, origin_state: int, destiny_state: int, callback: callable):
        """
        Add a transition between two states in the finite state machine.

        Args:
            origin_state (int): The ID of the origin state.
            destiny_state (int): The ID of the destiny state.
            callback (callable): The function that represents the transition condition.

        Raises:
            StateDeclarationError: If the origin_state or destiny_state is not an integer or callback is not callable.
            KeyError: If the origin_state is not found in the states.
        """
        if not isinstance(origin_state, int) or not isinstance(destiny_state, int) or not callable(callback):
            raise StateDeclarationError('Error on transition declaration: state_id -> int, callback -> func')

        if origin_state not in self.states:
            raise KeyError(f"State {origin_state} not found. Add state first!")

        self.states[origin_state]['transitions'].append({
            'destiny_state': destiny_state,
            'condition': callback
        })

    def start(self):
        """
        Start the finite state machine.
        """
        next(self.task_gen)

    def send(self, value_to_send):
        """
        Send a value to the finite state machine for processing.

        Args:
            value_to_send: The value to send for processing.
        """
        self.task_gen.send(value_to_send)

    def task(self):
        """
        The main task of the finite state machine.
        """
        self.current_state = 0
        exec_state_func = True
        while True:
            if exec_state_func: 
                self.states[self.current_state]['func']()
                exec_state_func = False
            value_to_transition = yield
            for transition in self.states[self.current_state]['transitions']:
                if transition['condition'](value_to_transition):
                    self.current_state = transition['destiny_state']
                    exec_state_func = True
                    break





fsm = FSM()
fsm.add_state(0, lambda: print('estado1'))
fsm.add_state(1, lambda: print('estado2'))
fsm.add_state(2, lambda: print('estado3'))
fsm.add_transition(0, 1, lambda received_number: True if received_number == 2 else False)
fsm.add_transition(1, 2, lambda received_number: True if received_number == 3 else False)
fsm.add_transition(2, 0, lambda received_number: True if received_number == 0 else False)
fsm.start()
fsm.send(2)
fsm.send(3)
fsm.send(0)
fsm.send(3)

# def generador():
#     i = 0
#     while True:
#         yield i 
#         i += 1
# g = generador()
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))

# def generador():
#     while True:
#         val = yield 
#         print(val)
# g = generador()
# next(g)
# g.send(1)
# print("HOla")
# g.send(2)
# g.send(3)
# g.send("n")
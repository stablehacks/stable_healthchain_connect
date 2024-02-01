# stateMachine.py

class StateMachine:
    def __init__(self, states):
        self.states = states
        self.current_state = None

    def set_state(self, state_name):
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' not found in the list of states.")
        self.current_state = state_name

    def run(self, callback=None):
        if self.current_state is None:
            raise ValueError("No initial state set. Call set_state() first.")

        for state_name in sorted(self.states.keys()):
            self.set_state(state_name)
            state_function = self.states[state_name]
            if callback:
                callback(f"Entering state {state_name}: {state_function.__doc__}")
            state_function()
            if callback:
                callback(f"Exiting state {state_name}: {state_function.__doc__}")



# Custom state functions
def state_1():
    import state1
    print("Entering state 1: Hello, State Machine! This is where things get set up for state 1")
    # Your state-specific logic goes here
    print("Exiting state 1: State 1 logic completed.")


def state_2():
    print("Entering state 2: Hello, State Machine! This is where things get updated for state 2")
    # Your state-specific logic goes here
    print("Exiting state 2: State 2 logic completed.")


def state_3():
    print("Entering state 3: Hello, State Machine! This is where checks are made for state 3")
    # Your state-specific logic goes here
    print("Exiting state 3: State 3 logic completed.")

# test.py
from stateMachine import StateMachine, state_1, state_2, state_3

if __name__ == "__main__":
    states = {
        '1': state_1,
        '2': state_2,
        '3': state_3
        # Add more states as needed
    }

    state_machine = StateMachine(states)

    # Set the initial state to '1'
    state_machine.set_state('1')

    # Run the state machine
    state_machine.run()

# todo: is 'pause' the right word choice here?
def _pause_connection() -> None:
    """
    This is a placeholder function to simulate a pause in the connection between the PEP and subject.
    It is triggered whenever a change in parameters is detected and the validity of the changed parameter
    needs to be checked before the connection is allowed to continue.
    """
    print('Change of parameters detected. Pausing connection until validity of parameters is confirmed.')
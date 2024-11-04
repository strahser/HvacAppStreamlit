import streamlit
from streamlit import session_state as _state

_PERSIST_STATE_KEY = f"{__name__}_PERSIST"


def persist(key: str) -> str:
    """Mark widget state as persistent."""
    if _PERSIST_STATE_KEY not in _state:
        _state[_PERSIST_STATE_KEY] = set()

    _state[_PERSIST_STATE_KEY].add(key)

    return key


def load_widget_state():
    """Load persistent widget state."""
    # if _PERSIST_STATE_KEY in _state:
    _state.update({
        key: value
        for key, value in _state.items()
        # if key in _state[_PERSIST_STATE_KEY]
    })


def _write_state():
    st_dict = {}
    for val in _state[_PERSIST_STATE_KEY]:
        if val in _state:
            st_dict[val] = _state[val]
        else:
            st_dict[val] = 1
    streamlit.write(st_dict)
    return st_dict

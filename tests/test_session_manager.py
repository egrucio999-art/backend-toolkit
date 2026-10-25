import time
from session_manager import SessionManager


def test_create_and_get():
    sm = SessionManager()
    sid = sm.create_session(user_id='u1')
    session = sm.get_session(sid)
    assert session is not None
    assert session['user_id'] == 'u1'


def test_delete():
    sm = SessionManager()
    sid = sm.create_session()
    assert sm.delete_session(sid) is True
    assert sm.get_session(sid) is None
    assert sm.delete_session(sid) is False


def test_cleanup_expired():
    sm = SessionManager()
    sid = sm.create_session()
    sm.sessions[sid]['last_activity'] = time.time() - 7200
    removed = sm.cleanup_sessions(timeout=3600)
    assert removed == 1
    assert sm.get_session(sid) is None

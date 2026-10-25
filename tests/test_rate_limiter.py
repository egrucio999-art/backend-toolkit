import time
from rate_limiter import RateLimiter


def test_allows_under_limit():
    rl = RateLimiter(max_requests=3, window=1)
    assert rl.allow('ip') is True
    assert rl.allow('ip') is True
    assert rl.allow('ip') is True


def test_blocks_over_limit():
    rl = RateLimiter(max_requests=2, window=1)
    rl.allow('ip')
    rl.allow('ip')
    assert rl.allow('ip') is False


def test_remaining_count():
    rl = RateLimiter(max_requests=5, window=60)
    rl.allow('ip')
    rl.allow('ip')
    assert rl.get_remaining('ip') == 3


def test_reset():
    rl = RateLimiter(max_requests=1, window=60)
    rl.allow('ip')
    assert rl.allow('ip') is False
    rl.reset('ip')
    assert rl.allow('ip') is True


def test_window_expiry():
    rl = RateLimiter(max_requests=1, window=0.2)
    rl.allow('ip')
    assert rl.allow('ip') is False
    time.sleep(0.3)
    assert rl.allow('ip') is True

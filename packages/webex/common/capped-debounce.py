import time

def debounce(fn, wait, options):
  if not callable(fn):
    raise ValueError('`fn` must be a function')

  if not wait:
    raise ValueError('`wait` is required')

  options = options or {}
  if 'maxWait' not in options:
    raise ValueError('`options.maxWait` is required')
  if 'maxCalls' not in options:
    raise ValueError('`options.maxCalls` is required')

  maxCalls = options['maxCalls']
  maxWait = options['maxWait']
  count = 0
  maxWaitTimer = None
  waitTimer = None

  def wrapper():
    nonlocal count, maxWaitTimer, waitTimer

    count += 1

    if waitTimer:
      waitTimer.cancel()
    waitTimer = Timer(wait, exec)

    if not maxWaitTimer:
      maxWaitTimer = Timer(maxWait, exec)

    if count >= maxCalls:
      exec()

  def exec():
    nonlocal count, maxWaitTimer, waitTimer

    if waitTimer:
      waitTimer.cancel()
    waitTimer = None
    if maxWaitTimer:
      maxWaitTimer.cancel()
    maxWaitTimer = None
    count = 0

    fn()

  return wrapper

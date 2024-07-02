import threading

def safe_set_timeout(callback, timeout):
  timer = threading.Timer(timeout / 1000, callback)
  timer.start()
  return timer

def safe_set_interval(callback, interval):
  def interval_wrapper():
    callback()
    safe_set_timeout(interval_wrapper, interval)
  timer = threading.Timer(interval / 1000, interval_wrapper)
  timer.start()
  return timer

class Timer:
  def __init__(self, callback, timeout):
    self.state = 'init'
    self.timeout = timeout
    self.callback = callback
    self.current_timer = None

  def start(self):
    if self.state != 'init':
      raise Exception(f"Can't start the timer when it's in {self.state} state")
    self.start_timer()
    self.state = 'running'

  def reset(self):
    if self.state != 'running':
      raise Exception(f"Can't reset the timer when it's in {self.state} state")
    self.clear_timer()
    self.start_timer()

  def cancel(self):
    if self.state != 'running':
      raise Exception(f"Can't cancel the timer when it's in {self.state} state")
    self.clear_timer()
    self.state = 'done'

  def start_timer(self):
    self.current_timer = safe_set_timeout(self.callback, self.timeout)

  def clear_timer(self):
    self.current_timer.cancel()

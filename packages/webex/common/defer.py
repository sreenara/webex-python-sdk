import asyncio

class Defer:
  def __init__(self):
    self.promise = asyncio.get_event_loop().create_future()

    def resolve(result):
      self.promise.set_result(result)

    def reject(error):
      self.promise.set_exception(error)

    self.resolve = resolve
    self.reject = reject

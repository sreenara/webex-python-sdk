import functools

def proxy_events(emitter, proxy):
  def proxy_wrapper(*args):
    getattr(emitter, args[0])(*args[1:])
    return proxy
  proxy.on = functools.partial(proxy_wrapper, 'on')
  proxy.once = functools.partial(proxy_wrapper, 'once')
  return emitter

def transfer_events(events, source, drain):
  events = events if isinstance(events, list) else [events]
  for event in events:
    if hasattr(source, 'on'):
      source.on(event, lambda *args: emit(drain, event, *args))

def emit(target, *args):
  method = getattr(target, 'trigger', None) or getattr(target, 'emit', None)
  if not method:
    raise Exception('Could not determine emit method')
  return method(*args)

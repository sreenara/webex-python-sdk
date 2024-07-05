def tap(fn):
  def wrapper(r):
    fn(r)
    return r
  return wrapper

# Example usage
def f():
  return 5

result = tap(lambda: print(12))(f())
print(result)  # Output: 5

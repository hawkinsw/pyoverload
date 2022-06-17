from pyoverload import overload

@overload
def add(a: int, b: int) -> int:
  return a + b

@overload
def add(b: int, a: str) -> int:
  return str(b) + ": " + a

if __name__=="__main__":
  print(f"{add(5, 6)=}")
  print(f"{add(5, 'testing')=}")

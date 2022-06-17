
from collections import abc
from re import I
from tokenize import Number
from typing import Any, Callable, Iterator, Mapping, Tuple, Type, List

class _OverloadInstance:
  def __init__(self, name: str, protocol: Tuple[Type], implementation: Callable) -> None:
    self.name = name
    self.protocol = protocol
    self.implementation = implementation

  def matches(self, args: Tuple[Any]) -> bool:
    for i, j in zip(self.protocol, args):
      if i != type(j):
        return False
    return True

  def invoke(self, args, kwargs) -> Any:
    return self.implementation(*args, **kwargs)

class _OverloadedFunction:
  name: str
  instances: List[_OverloadInstance]

  def __init__(self, name: str):
    self.name = name
    self.instances = []

  def add_instance(self, instance: _OverloadInstance) -> None:
    self.instances.append(instance)

  def invoke(self, args, kwargs) -> Any:
    for instance in self.instances:
      if instance.matches(args):
        return instance.invoke(args, kwargs)

class _OverloadHandler(abc.MutableMapping):
  overloaded_functions: Mapping[str, _OverloadedFunction]
  def __init__(self):
    self.overloaded_functions = {} 

  def __getitem__(self, k: str) -> _OverloadedFunction:
    return self.overloaded_functions.__getitem__(k)

  def __setitem__(self, __k: str, __v: _OverloadedFunction) -> None:
    return self.overloaded_functions.__setitem__(__k, __v)

  def __delitem__(self, k: str) -> Any:
    return self.overloaded_functions.__delattr__(k)

  def __iter__(self) -> Iterator:
    return self.overloaded_functions.__iter__()

  def __len__(self) -> Number:
    return self. overloaded_functions.__len__()

  def named_resolver(self, name) -> Callable:
    def resolver(*args, **kwargs) -> Any:
      if name not in self.overloaded_functions:
        raise NameError
      of: _OverloadedFunction = self.overloaded_functions[name]
      return of.invoke(args, kwargs)
    return resolver

global_olh = _OverloadHandler()

def overload(overloaded: Callable):
  annotations = tuple(list(overloaded.__annotations__.values())[:-1])
  oi = _OverloadInstance(overloaded.__name__,  annotations, overloaded)
  of = None
  if oi.name in global_olh:
    of = global_olh[oi.name]
  else:
    of = _OverloadedFunction(oi.name)
    global_olh[oi.name] = of
  
  of.add_instance(oi)
  return global_olh.named_resolver(overloaded.__name__)
compose
=======

Usage
-----

```python
import compose

l = [1,2,3]
thread(lambda x: x**2,
       *l,
       monad=compose_m(logging_m(),list_m()))
```

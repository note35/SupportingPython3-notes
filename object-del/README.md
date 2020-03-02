This is just a simple note related to the different behavior of `__del__` function in Python2/3.

I was hitting this issue after migrating one of the package written as similar as **script.py**.

- In Python2, `__del__` will be executed earlier (almost right after the script), therefore, it's close to the concept of destructor in C/C++, you can expect your object is free right after your script execution.
- In Python3, `__del__` will be executed later (you won't know the time in any line of the script)

Due to above facts, you may write expected code in `__del__` in Python2, but you need to move them to the **"known timing" place** in Python3. Although in some case, Python3 may do garbage collection as early as Python2 does. Overall, the interpreter has never promised the timing of garbage collection, although the pattern might work in Python2 and even in Python3, you should avoid writing code inside `__del__`.

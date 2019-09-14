# Python 2/3 extension example

This is a extended python2/3 compatible version of physacco's hello world example. The original work was done by physacco in [gist](https://gist.github.com/physacco/2e1b52415f3a964ad2a542a99bebed8f).

## Build

You can use the convenient script...

```
$ ./build.sh
```

Or run the command by yourself

```
$ pythonX.Y setup.py build
```

## Run

```
$ cd build/lib...-X.Y
$ pythonX.Y
>>> import hello
>>> hello.hello_world()
Hello, world!
>>> hello.handle_int(1234)
1234
>>> hello.handle_python2_str('あ')
b'\xe3\x81\x82'
```

## References

- [Python 3 extension example](https://gist.github.com/physacco/2e1b52415f3a964ad2a542a99bebed8f)
- [Migrating C extensions](http://python3porting.com/cextensions.html)
- [Threads and Callbacks for Embedded Python](https://www.slideshare.net/YiLungTsai/embed-python)

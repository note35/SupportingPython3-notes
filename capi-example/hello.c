/*
    Original version: https://gist.github.com/physacco/2e1b52415f3a964ad2a542a99bebed8f

    This is a extended python2/3 compatible version of physacco's hello world example
    http://python3porting.com/cextensions.html
*/

#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <Python.h>

#define HELLO_MODULE_NAME   "hello"
#define HELLO_MODULE_DOC    "A python2/3 compatible version of hello world example"

// Module method definitions
static PyObject* hello_world(PyObject *self, PyObject *args) {
    /*
    Does this function need comment?
    */
    printf("Hello, world!\n");
    Py_RETURN_NONE;
}

#if PY_MAJOR_VERSION >= 3
#define PyInt_FromLong(x) PyLong_FromLong(x)
#endif
static PyObject* handle_int(PyObject *self, PyObject *args) {
    /*
    https://docs.python.org/2/c-api/int.html
    Python3's C-API doesn't have PyInt_ functions
    >>> import sys
    >>> hello.handle_long(sys.maxsize)
    9223372036854775807
    */
    long ret;
    if (!PyArg_ParseTuple(args, "l", &ret)) {
        return NULL;
    }
    return PyInt_FromLong(ret);
}

#if PY_MAJOR_VERSION >= 3
#define Py2str_FromStringAndSize(x, y) PyBytes_FromStringAndSize(x, y)
#else
#define Py2str_FromStringAndSize(x, y) PyString_FromStringAndSize(x, y)
#endif
static PyObject* handle_python2_str(PyObject *self, PyObject *args) {
    /*
    Python2 hanlde string as bytes, this function makes python3 has the same function with python2 str behavior
    >>> import hello
    >>> hello.handle_python2_str('ㄇ')
    b'\xe3\x84\x87'
    */
    const char* ret;
    if (!PyArg_ParseTuple(args, "s", &ret)) {
        return NULL;
    }
    return Py2str_FromStringAndSize(ret, strlen(ret));
}

char program[] =
    "import time\n"
    "print('Child thread is running')\n"
    "time.sleep(1)\n"
    "print('Child thread is finished')\n";

void* rpf(void *arg){
    PyGILState_STATE gstate = PyGILState_Ensure();

    PyRun_SimpleString(program);

    PyGILState_Release(gstate);
    pthread_exit(NULL);
    return NULL;
}

static PyObject* call_threading(PyObject *self, PyObject *args){
    /* A simple multiple threading example in C with GIL */
    PyEval_InitThreads();
    PyThreadState *save = PyEval_SaveThread();

    pthread_t tid1, tid2;
    char *tname1 = "worker1";
    char *tname2 = "worker2";
    pthread_create(&tid1, NULL, &rpf, &tname1);
    pthread_create(&tid2, NULL, &rpf, &tname2);

    printf("Main thread is running\n");

    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    PyEval_RestoreThread(save);

    printf("Main thread is finished\n");

    Py_RETURN_NONE;
}

// Method definition object for this extension, these argumens mean:
// ml_name: The name of the method
// ml_meth: Function pointer to the method implementation
// ml_flags: Flags indicating special features of this method, such as
//          accepting arguments, accepting keyword arguments, being a
//          class method, or being a static method of a class.
// ml_doc:  Contents of this method's docstring
static PyMethodDef hello_methods[] = {
    {
        "hello_world", hello_world, METH_NOARGS,
        "Print 'hello world' from a method defined in a C extension."
    },
    {
        "handle_int", handle_int, METH_VARARGS,
        "handle int properly in both python2 and python3."
    },
    {
        "handle_python2_str", handle_python2_str, METH_VARARGS,
        "handle bytes properly in both python2 and python3."
    },
    {
        "call_threading", call_threading, METH_VARARGS,
        "call thread from c"
    },
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
// Module definition
// The arguments of this structure tell Python what to call your extension,
// what it's methods are and where to look for it's method definitions
static struct PyModuleDef hello_definition = {
    PyModuleDef_HEAD_INIT,
    HELLO_MODULE_NAME,
    HELLO_MODULE_DOC,
    -1,
    hello_methods
};

// Module initialization
// Python calls this function when importing your extension. It is important
// that this function is named PyInit_[[your_module_name]] exactly, and matches
// the name keyword argument in setup.py's setup() call.
PyMODINIT_FUNC PyInit_hello(void) {
    Py_Initialize();
    return PyModule_Create(&hello_definition);
}

#else
PyMODINIT_FUNC inithello(void) {
    Py_InitModule3(HELLO_MODULE_NAME, hello_methods, HELLO_MODULE_DOC);
}

#endif

#include "Python.h"

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

Py_buffer *get_new_buffer(int nitems, int itemsize, char *fmt) {
    Py_buffer *buf = (Py_buffer *) malloc(sizeof(*buf));
    buf->obj = NULL;
    buf->buf = PyMem_Malloc(nitems * itemsize);
    buf->len = nitems * itemsize;
    buf->readonly = 0;
    buf->itemsize = itemsize;
    buf->format = fmt;
    buf->ndim = 1;
    buf->shape = NULL;
    buf->strides = NULL;
    buf->suboffsets = NULL;
    buf->internal = NULL;
    return buf;
}

static PyObject *
intersect_lists_extension(PyObject *m, PyObject *args) {
    PyObject* list;
    if (!PyArg_ParseTuple(args, "O", &list))
        return NULL;
    Py_INCREF(list);

    if (!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "arg must be list");
        return NULL;
    }

    int i, min_len;
    Py_ssize_t lists_len;
    lists_len = PyList_Size(list);
    int **my_arrays = (int **)PyMem_Malloc(lists_len * sizeof(Py_ssize_t));
    if (my_arrays == NULL)
        return PyErr_NoMemory();

    int *pointers = (int *)PyMem_Malloc(lists_len * sizeof(Py_ssize_t));
    if (pointers == NULL)
        return PyErr_NoMemory();

    int *list_lens = (int *)PyMem_Malloc(lists_len * sizeof(Py_ssize_t));
    if (list_lens == NULL)
        return PyErr_NoMemory();

    for (i = 0; i < lists_len; i++) {
        PyObject *array = PyList_GetItem(list, i);
#if PY_MAJOR_VERSION >= 3
        Py_buffer array_buffer;
        if (PyObject_CheckBuffer(array)) {
            PyObject_GetBuffer(array, &array_buffer, PyBUF_SIMPLE);
        } else {
            PyErr_SetString(PyExc_TypeError,
                "list elements have to support the buffer protocol");
            return NULL;
        }

        int *array_ptr = array_buffer.buf;
        int array_len = array_buffer.len / array_buffer.itemsize;
#else
        PyObject *buffer_info = PyObject_CallMethod(array, "buffer_info", NULL);
        int *array_ptr = NULL, array_len;
        PyArg_ParseTuple(buffer_info, "li", &array_ptr, &array_len);
#endif
        pointers[i] = 0;
        if (array_len > 0) {
            my_arrays[i] = array_ptr;
            list_lens[i] = array_len;
            if (i == 0 || array_len < min_len)
                min_len = array_len;
        } else {
            PyMem_Free(my_arrays);
            PyMem_Free(pointers);
            PyMem_Free(list_lens);
#if PY_MAJOR_VERSION >= 3
            Py_buffer *intersection_buffer = get_new_buffer(0, sizeof(int), "d");
            return PyMemoryView_FromBuffer(intersection_buffer);
#else
            return PyList_New(0);
#endif
        }
    }

    int intersection_idx = 0;
#if PY_MAJOR_VERSION >= 3
    Py_buffer *intersection_buffer = get_new_buffer(min_len, sizeof(int), "i");
    int *intersection = intersection_buffer->buf;
#else
    PyObject *intersection = PyList_New(0);
#endif

    int min_val = -1, min_idx = -1, tmp_val = -1, all_same;

    int counter = 0;
    int not_finished = 1;
    while(not_finished) {
        all_same = 1;
        for (i = 0; i < lists_len; i++) {
            tmp_val = my_arrays[i][pointers[i]];
            if (i > 0) {
                if (tmp_val < min_val) {
                    min_val = tmp_val;
                    min_idx = i;
                    all_same = 0;
                } else {
                    if (tmp_val > min_val)
                        all_same = 0;
                }
            } else {
                min_val = tmp_val;
                min_idx = i;
            }
        }
        if (all_same == 1) {
#if PY_MAJOR_VERSION >= 3
            intersection[intersection_idx] = min_val;
#else
            PyObject *item = PyInt_FromLong(min_val);
            PyList_Append(intersection, item);
            Py_DECREF(item);
#endif
            intersection_idx++;
            for (i = 0; i < lists_len; i++) {
                pointers[i]++;
                if (pointers[i] >= list_lens[i]) {
                    not_finished = 0;
                }
            }
        } else {
            pointers[min_idx]++;
            if (pointers[min_idx] >= list_lens[min_idx]) {
                not_finished = 0;
            }
        }
        counter++;
    }

    PyMem_Free(my_arrays);
    PyMem_Free(pointers);
    PyMem_Free(list_lens);
#if PY_MAJOR_VERSION >= 3
    long nbytes = intersection_idx * intersection_buffer->itemsize;
    //PyMem_Realloc(intersection_buffer->buf, nbytes);
    intersection_buffer->len = nbytes;
    return PyMemoryView_FromBuffer(intersection_buffer);
#else
    return intersection;
#endif
}

static PyMethodDef posting_lists_extension_methods[] = {
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {"intersect_lists_extension", (PyCFunction)intersect_lists_extension,
     METH_VARARGS, "Return intersection of lists"},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int posting_lists_extension_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int posting_lists_extension_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "posting_lists_extension",
        NULL,
        sizeof(struct module_state),
        posting_lists_extension_methods,
        NULL,
        posting_lists_extension_traverse,
        posting_lists_extension_clear,
        NULL
};

#define INITERROR return NULL

PyObject *
PyInit_posting_lists_extension(void)

#else
#define INITERROR return

void
initposting_lists_extension(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("posting_lists_extension", posting_lists_extension_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("posting_lists_extension.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}

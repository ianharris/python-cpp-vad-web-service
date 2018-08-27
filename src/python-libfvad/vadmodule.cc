#include <Python.h>
#include <iostream>
#include "libfvad_module.h"

static VADProcessor *vad = NULL;

static PyObject * setsamplerate(PyObject *self, PyObject *args)
{
    int samplerate, result;

    if(!PyArg_ParseTuple(args, "i", &samplerate)) {
        return NULL;
    }
    
    result = vad->setSampleRate(samplerate);
    return Py_BuildValue("i", result);
}

static PyObject * setmode(PyObject *self, PyObject *args)
{
    int mode, result;

    if(!PyArg_ParseTuple(args, "i", &mode)) {
        return NULL;
    }
    
    result = vad->setMode(mode);
    return Py_BuildValue("i", result);
}

static PyObject * process(PyObject *self, PyObject *args)
{
    Py_buffer buffer;
    int result;

    if(!PyArg_ParseTuple(args, "y*", &buffer)) {
        return NULL;
    }
    // std::cout << "About to call vad->process" << std::endl;
    result = vad->process((int16_t *)buffer.buf,
                          (buffer.len) / 2);
    return Py_BuildValue("i", result);
}

static PyMethodDef VADMethods[] = { 
    {"setsamplerate",  setsamplerate, METH_VARARGS, "Set the sample rate of the underlying VAD analyser."},
    {"setmode",  setmode, METH_VARARGS, "Set the mode of the underlying VAD analyser."},
    {"process",  process, METH_VARARGS,"Process some audio with the underlying VAD analyser."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef vadmodule = { 
    PyModuleDef_HEAD_INIT,
    "iharrisvad",                           /* name of module */
    "Module for Voice Activity Detection",  /* module documentation */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    VADMethods
};

PyMODINIT_FUNC PyInit_iharrisvad(void)
{
    vad = new VADProcessor();
    return PyModule_Create(&vadmodule);
}

// static PyObject *
// spam_system(PyObject *self, PyObject *args)
// {
//     const char *command;
//     int sts;
// 
//     if (!PyArg_ParseTuple(args, "s", &command))
//         return NULL;
//     sts = system(command);
//     return Py_BuildValue("i", sts);
// }

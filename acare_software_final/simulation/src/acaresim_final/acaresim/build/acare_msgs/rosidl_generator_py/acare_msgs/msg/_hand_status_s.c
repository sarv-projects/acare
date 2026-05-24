// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "acare_msgs/msg/detail/hand_status__struct.h"
#include "acare_msgs/msg/detail/hand_status__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool acare_msgs__msg__hand_status__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[39];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("acare_msgs.msg._hand_status.HandStatus", full_classname_dest, 38) == 0);
  }
  acare_msgs__msg__HandStatus * ros_message = _ros_message;
  {  // hand_detected
    PyObject * field = PyObject_GetAttrString(_pymsg, "hand_detected");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->hand_detected = (Py_True == field);
    Py_DECREF(field);
  }
  {  // is_open
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_open");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_open = (Py_True == field);
    Py_DECREF(field);
  }
  {  // palm_up
    PyObject * field = PyObject_GetAttrString(_pymsg, "palm_up");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->palm_up = (Py_True == field);
    Py_DECREF(field);
  }
  {  // x
    PyObject * field = PyObject_GetAttrString(_pymsg, "x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->x = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // y
    PyObject * field = PyObject_GetAttrString(_pymsg, "y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->y = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // z
    PyObject * field = PyObject_GetAttrString(_pymsg, "z");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->z = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // confidence
    PyObject * field = PyObject_GetAttrString(_pymsg, "confidence");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->confidence = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * acare_msgs__msg__hand_status__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of HandStatus */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("acare_msgs.msg._hand_status");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "HandStatus");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  acare_msgs__msg__HandStatus * ros_message = (acare_msgs__msg__HandStatus *)raw_ros_message;
  {  // hand_detected
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->hand_detected ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "hand_detected", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // is_open
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_open ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_open", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // palm_up
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->palm_up ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "palm_up", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // z
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->z);
    {
      int rc = PyObject_SetAttrString(_pymessage, "z", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // confidence
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->confidence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "confidence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

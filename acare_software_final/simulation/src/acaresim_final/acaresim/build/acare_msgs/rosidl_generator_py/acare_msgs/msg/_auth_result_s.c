// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from acare_msgs:msg/AuthResult.idl
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
#include "acare_msgs/msg/detail/auth_result__struct.h"
#include "acare_msgs/msg/detail/auth_result__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool acare_msgs__msg__auth_result__convert_from_py(PyObject * _pymsg, void * _ros_message)
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
    assert(strncmp("acare_msgs.msg._auth_result.AuthResult", full_classname_dest, 38) == 0);
  }
  acare_msgs__msg__AuthResult * ros_message = _ros_message;
  {  // user_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "user_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->user_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // name
    PyObject * field = PyObject_GetAttrString(_pymsg, "name");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->name, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // role
    PyObject * field = PyObject_GetAttrString(_pymsg, "role");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->role, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // success
    PyObject * field = PyObject_GetAttrString(_pymsg, "success");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->success = (Py_True == field);
    Py_DECREF(field);
  }
  {  // face_verified
    PyObject * field = PyObject_GetAttrString(_pymsg, "face_verified");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->face_verified = (Py_True == field);
    Py_DECREF(field);
  }
  {  // face_confidence
    PyObject * field = PyObject_GetAttrString(_pymsg, "face_confidence");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->face_confidence = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // voice_confidence
    PyObject * field = PyObject_GetAttrString(_pymsg, "voice_confidence");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->voice_confidence = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * acare_msgs__msg__auth_result__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of AuthResult */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("acare_msgs.msg._auth_result");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "AuthResult");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  acare_msgs__msg__AuthResult * ros_message = (acare_msgs__msg__AuthResult *)raw_ros_message;
  {  // user_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->user_id.data,
      strlen(ros_message->user_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "user_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // name
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->name.data,
      strlen(ros_message->name.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "name", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // role
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->role.data,
      strlen(ros_message->role.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "role", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // success
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->success ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "success", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // face_verified
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->face_verified ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "face_verified", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // face_confidence
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->face_confidence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "face_confidence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // voice_confidence
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->voice_confidence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "voice_confidence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

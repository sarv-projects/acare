// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from acare_msgs:msg/LogEvent.idl
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
#include "acare_msgs/msg/detail/log_event__struct.h"
#include "acare_msgs/msg/detail/log_event__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool acare_msgs__msg__log_event__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[35];
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
    assert(strncmp("acare_msgs.msg._log_event.LogEvent", full_classname_dest, 34) == 0);
  }
  acare_msgs__msg__LogEvent * ros_message = _ros_message;
  {  // event_type
    PyObject * field = PyObject_GetAttrString(_pymsg, "event_type");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->event_type, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
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
  {  // tool
    PyObject * field = PyObject_GetAttrString(_pymsg, "tool");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->tool, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // state
    PyObject * field = PyObject_GetAttrString(_pymsg, "state");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->state, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // description
    PyObject * field = PyObject_GetAttrString(_pymsg, "description");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->description, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // timestamp
    PyObject * field = PyObject_GetAttrString(_pymsg, "timestamp");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->timestamp = PyLong_AsLongLong(field);
    Py_DECREF(field);
  }
  {  // voice_e2e_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "voice_e2e_ms");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->voice_e2e_ms = PyLong_AsLongLong(field);
    Py_DECREF(field);
  }
  {  // vision_search_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "vision_search_ms");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->vision_search_ms = PyLong_AsLongLong(field);
    Py_DECREF(field);
  }
  {  // motion_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "motion_ms");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->motion_ms = PyLong_AsLongLong(field);
    Py_DECREF(field);
  }
  {  // total_task_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "total_task_ms");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->total_task_ms = PyLong_AsLongLong(field);
    Py_DECREF(field);
  }
  {  // safety_severity
    PyObject * field = PyObject_GetAttrString(_pymsg, "safety_severity");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->safety_severity, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * acare_msgs__msg__log_event__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of LogEvent */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("acare_msgs.msg._log_event");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "LogEvent");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  acare_msgs__msg__LogEvent * ros_message = (acare_msgs__msg__LogEvent *)raw_ros_message;
  {  // event_type
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->event_type.data,
      strlen(ros_message->event_type.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "event_type", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
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
  {  // tool
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->tool.data,
      strlen(ros_message->tool.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "tool", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // state
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->state.data,
      strlen(ros_message->state.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // description
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->description.data,
      strlen(ros_message->description.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "description", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // timestamp
    PyObject * field = NULL;
    field = PyLong_FromLongLong(ros_message->timestamp);
    {
      int rc = PyObject_SetAttrString(_pymessage, "timestamp", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // voice_e2e_ms
    PyObject * field = NULL;
    field = PyLong_FromLongLong(ros_message->voice_e2e_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "voice_e2e_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // vision_search_ms
    PyObject * field = NULL;
    field = PyLong_FromLongLong(ros_message->vision_search_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "vision_search_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // motion_ms
    PyObject * field = NULL;
    field = PyLong_FromLongLong(ros_message->motion_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "motion_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // total_task_ms
    PyObject * field = NULL;
    field = PyLong_FromLongLong(ros_message->total_task_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "total_task_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // safety_severity
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->safety_severity.data,
      strlen(ros_message->safety_severity.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "safety_severity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

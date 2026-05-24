// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "acare_msgs/srv/detail/enrol_staff__rosidl_typesupport_introspection_c.h"
#include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "acare_msgs/srv/detail/enrol_staff__functions.h"
#include "acare_msgs/srv/detail/enrol_staff__struct.h"


// Include directives for member types
// Member `name`
// Member `role`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  acare_msgs__srv__EnrolStaff_Request__init(message_memory);
}

void acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_fini_function(void * message_memory)
{
  acare_msgs__srv__EnrolStaff_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_member_array[2] = {
  {
    "name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Request, name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "role",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Request, role),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_members = {
  "acare_msgs__srv",  // message namespace
  "EnrolStaff_Request",  // message name
  2,  // number of fields
  sizeof(acare_msgs__srv__EnrolStaff_Request),
  false,  // has_any_key_member_
  acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_member_array,  // message members
  acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_type_support_handle = {
  0,
  &acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Request__get_type_hash,
  &acare_msgs__srv__EnrolStaff_Request__get_type_description,
  &acare_msgs__srv__EnrolStaff_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Request)() {
  if (!acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_type_support_handle.typesupport_identifier) {
    acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__rosidl_typesupport_introspection_c.h"
// already included above
// #include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__functions.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__struct.h"


// Include directives for member types
// Member `staff_id`
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  acare_msgs__srv__EnrolStaff_Response__init(message_memory);
}

void acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_fini_function(void * message_memory)
{
  acare_msgs__srv__EnrolStaff_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_member_array[3] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "staff_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Response, staff_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_members = {
  "acare_msgs__srv",  // message namespace
  "EnrolStaff_Response",  // message name
  3,  // number of fields
  sizeof(acare_msgs__srv__EnrolStaff_Response),
  false,  // has_any_key_member_
  acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_member_array,  // message members
  acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle = {
  0,
  &acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Response__get_type_hash,
  &acare_msgs__srv__EnrolStaff_Response__get_type_description,
  &acare_msgs__srv__EnrolStaff_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Response)() {
  if (!acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle.typesupport_identifier) {
    acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__rosidl_typesupport_introspection_c.h"
// already included above
// #include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__functions.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "acare_msgs/srv/enrol_staff.h"
// Member `request`
// Member `response`
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  acare_msgs__srv__EnrolStaff_Event__init(message_memory);
}

void acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_fini_function(void * message_memory)
{
  acare_msgs__srv__EnrolStaff_Event__fini(message_memory);
}

size_t acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__size_function__EnrolStaff_Event__request(
  const void * untyped_member)
{
  const acare_msgs__srv__EnrolStaff_Request__Sequence * member =
    (const acare_msgs__srv__EnrolStaff_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_const_function__EnrolStaff_Event__request(
  const void * untyped_member, size_t index)
{
  const acare_msgs__srv__EnrolStaff_Request__Sequence * member =
    (const acare_msgs__srv__EnrolStaff_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_function__EnrolStaff_Event__request(
  void * untyped_member, size_t index)
{
  acare_msgs__srv__EnrolStaff_Request__Sequence * member =
    (acare_msgs__srv__EnrolStaff_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__fetch_function__EnrolStaff_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const acare_msgs__srv__EnrolStaff_Request * item =
    ((const acare_msgs__srv__EnrolStaff_Request *)
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_const_function__EnrolStaff_Event__request(untyped_member, index));
  acare_msgs__srv__EnrolStaff_Request * value =
    (acare_msgs__srv__EnrolStaff_Request *)(untyped_value);
  *value = *item;
}

void acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__assign_function__EnrolStaff_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  acare_msgs__srv__EnrolStaff_Request * item =
    ((acare_msgs__srv__EnrolStaff_Request *)
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_function__EnrolStaff_Event__request(untyped_member, index));
  const acare_msgs__srv__EnrolStaff_Request * value =
    (const acare_msgs__srv__EnrolStaff_Request *)(untyped_value);
  *item = *value;
}

bool acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__resize_function__EnrolStaff_Event__request(
  void * untyped_member, size_t size)
{
  acare_msgs__srv__EnrolStaff_Request__Sequence * member =
    (acare_msgs__srv__EnrolStaff_Request__Sequence *)(untyped_member);
  acare_msgs__srv__EnrolStaff_Request__Sequence__fini(member);
  return acare_msgs__srv__EnrolStaff_Request__Sequence__init(member, size);
}

size_t acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__size_function__EnrolStaff_Event__response(
  const void * untyped_member)
{
  const acare_msgs__srv__EnrolStaff_Response__Sequence * member =
    (const acare_msgs__srv__EnrolStaff_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_const_function__EnrolStaff_Event__response(
  const void * untyped_member, size_t index)
{
  const acare_msgs__srv__EnrolStaff_Response__Sequence * member =
    (const acare_msgs__srv__EnrolStaff_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_function__EnrolStaff_Event__response(
  void * untyped_member, size_t index)
{
  acare_msgs__srv__EnrolStaff_Response__Sequence * member =
    (acare_msgs__srv__EnrolStaff_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__fetch_function__EnrolStaff_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const acare_msgs__srv__EnrolStaff_Response * item =
    ((const acare_msgs__srv__EnrolStaff_Response *)
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_const_function__EnrolStaff_Event__response(untyped_member, index));
  acare_msgs__srv__EnrolStaff_Response * value =
    (acare_msgs__srv__EnrolStaff_Response *)(untyped_value);
  *value = *item;
}

void acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__assign_function__EnrolStaff_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  acare_msgs__srv__EnrolStaff_Response * item =
    ((acare_msgs__srv__EnrolStaff_Response *)
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_function__EnrolStaff_Event__response(untyped_member, index));
  const acare_msgs__srv__EnrolStaff_Response * value =
    (const acare_msgs__srv__EnrolStaff_Response *)(untyped_value);
  *item = *value;
}

bool acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__resize_function__EnrolStaff_Event__response(
  void * untyped_member, size_t size)
{
  acare_msgs__srv__EnrolStaff_Response__Sequence * member =
    (acare_msgs__srv__EnrolStaff_Response__Sequence *)(untyped_member);
  acare_msgs__srv__EnrolStaff_Response__Sequence__fini(member);
  return acare_msgs__srv__EnrolStaff_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Event, request),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__size_function__EnrolStaff_Event__request,  // size() function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_const_function__EnrolStaff_Event__request,  // get_const(index) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_function__EnrolStaff_Event__request,  // get(index) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__fetch_function__EnrolStaff_Event__request,  // fetch(index, &value) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__assign_function__EnrolStaff_Event__request,  // assign(index, value) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__resize_function__EnrolStaff_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(acare_msgs__srv__EnrolStaff_Event, response),  // bytes offset in struct
    NULL,  // default value
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__size_function__EnrolStaff_Event__response,  // size() function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_const_function__EnrolStaff_Event__response,  // get_const(index) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__get_function__EnrolStaff_Event__response,  // get(index) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__fetch_function__EnrolStaff_Event__response,  // fetch(index, &value) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__assign_function__EnrolStaff_Event__response,  // assign(index, value) function pointer
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__resize_function__EnrolStaff_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_members = {
  "acare_msgs__srv",  // message namespace
  "EnrolStaff_Event",  // message name
  3,  // number of fields
  sizeof(acare_msgs__srv__EnrolStaff_Event),
  false,  // has_any_key_member_
  acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_member_array,  // message members
  acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_type_support_handle = {
  0,
  &acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_members,
  get_message_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Event__get_type_hash,
  &acare_msgs__srv__EnrolStaff_Event__get_type_description,
  &acare_msgs__srv__EnrolStaff_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Event)() {
  acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Request)();
  acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Response)();
  if (!acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_type_support_handle.typesupport_identifier) {
    acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "acare_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_members = {
  "acare_msgs__srv",  // service namespace
  "EnrolStaff",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_type_support_handle,
  NULL,  // response message
  // acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle
  NULL  // event_message
  // acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle
};


static rosidl_service_type_support_t acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_type_support_handle = {
  0,
  &acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_members,
  get_service_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Request__rosidl_typesupport_introspection_c__EnrolStaff_Request_message_type_support_handle,
  &acare_msgs__srv__EnrolStaff_Response__rosidl_typesupport_introspection_c__EnrolStaff_Response_message_type_support_handle,
  &acare_msgs__srv__EnrolStaff_Event__rosidl_typesupport_introspection_c__EnrolStaff_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    acare_msgs,
    srv,
    EnrolStaff
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    acare_msgs,
    srv,
    EnrolStaff
  ),
  &acare_msgs__srv__EnrolStaff__get_type_hash,
  &acare_msgs__srv__EnrolStaff__get_type_description,
  &acare_msgs__srv__EnrolStaff__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_acare_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff)(void) {
  if (!acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_type_support_handle.typesupport_identifier) {
    acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Event)()->data;
  }

  return &acare_msgs__srv__detail__enrol_staff__rosidl_typesupport_introspection_c__EnrolStaff_service_type_support_handle;
}

// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/srv/enrol_staff.h"


#ifndef ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__STRUCT_H_
#define ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
// Member 'role'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/EnrolStaff in the package acare_msgs.
typedef struct acare_msgs__srv__EnrolStaff_Request
{
  rosidl_runtime_c__String name;
  rosidl_runtime_c__String role;
} acare_msgs__srv__EnrolStaff_Request;

// Struct for a sequence of acare_msgs__srv__EnrolStaff_Request.
typedef struct acare_msgs__srv__EnrolStaff_Request__Sequence
{
  acare_msgs__srv__EnrolStaff_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__srv__EnrolStaff_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'staff_id'
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/EnrolStaff in the package acare_msgs.
typedef struct acare_msgs__srv__EnrolStaff_Response
{
  bool success;
  rosidl_runtime_c__String staff_id;
  rosidl_runtime_c__String message;
} acare_msgs__srv__EnrolStaff_Response;

// Struct for a sequence of acare_msgs__srv__EnrolStaff_Response.
typedef struct acare_msgs__srv__EnrolStaff_Response__Sequence
{
  acare_msgs__srv__EnrolStaff_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__srv__EnrolStaff_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  acare_msgs__srv__EnrolStaff_Event__request__MAX_SIZE = 1
};
// response
enum
{
  acare_msgs__srv__EnrolStaff_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/EnrolStaff in the package acare_msgs.
typedef struct acare_msgs__srv__EnrolStaff_Event
{
  service_msgs__msg__ServiceEventInfo info;
  acare_msgs__srv__EnrolStaff_Request__Sequence request;
  acare_msgs__srv__EnrolStaff_Response__Sequence response;
} acare_msgs__srv__EnrolStaff_Event;

// Struct for a sequence of acare_msgs__srv__EnrolStaff_Event.
typedef struct acare_msgs__srv__EnrolStaff_Event__Sequence
{
  acare_msgs__srv__EnrolStaff_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} acare_msgs__srv__EnrolStaff_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__STRUCT_H_

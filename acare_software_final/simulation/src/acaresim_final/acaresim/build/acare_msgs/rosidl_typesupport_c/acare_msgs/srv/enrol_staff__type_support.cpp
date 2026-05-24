// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "acare_msgs/srv/detail/enrol_staff__struct.h"
#include "acare_msgs/srv/detail/enrol_staff__type_support.h"
#include "acare_msgs/srv/detail/enrol_staff__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace acare_msgs
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _EnrolStaff_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EnrolStaff_Request_type_support_ids_t;

static const _EnrolStaff_Request_type_support_ids_t _EnrolStaff_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _EnrolStaff_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EnrolStaff_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EnrolStaff_Request_type_support_symbol_names_t _EnrolStaff_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, srv, EnrolStaff_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Request)),
  }
};

typedef struct _EnrolStaff_Request_type_support_data_t
{
  void * data[2];
} _EnrolStaff_Request_type_support_data_t;

static _EnrolStaff_Request_type_support_data_t _EnrolStaff_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EnrolStaff_Request_message_typesupport_map = {
  2,
  "acare_msgs",
  &_EnrolStaff_Request_message_typesupport_ids.typesupport_identifier[0],
  &_EnrolStaff_Request_message_typesupport_symbol_names.symbol_name[0],
  &_EnrolStaff_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t EnrolStaff_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EnrolStaff_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Request__get_type_hash,
  &acare_msgs__srv__EnrolStaff_Request__get_type_description,
  &acare_msgs__srv__EnrolStaff_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace acare_msgs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, acare_msgs, srv, EnrolStaff_Request)() {
  return &::acare_msgs::srv::rosidl_typesupport_c::EnrolStaff_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__struct.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__type_support.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace acare_msgs
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _EnrolStaff_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EnrolStaff_Response_type_support_ids_t;

static const _EnrolStaff_Response_type_support_ids_t _EnrolStaff_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _EnrolStaff_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EnrolStaff_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EnrolStaff_Response_type_support_symbol_names_t _EnrolStaff_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, srv, EnrolStaff_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Response)),
  }
};

typedef struct _EnrolStaff_Response_type_support_data_t
{
  void * data[2];
} _EnrolStaff_Response_type_support_data_t;

static _EnrolStaff_Response_type_support_data_t _EnrolStaff_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EnrolStaff_Response_message_typesupport_map = {
  2,
  "acare_msgs",
  &_EnrolStaff_Response_message_typesupport_ids.typesupport_identifier[0],
  &_EnrolStaff_Response_message_typesupport_symbol_names.symbol_name[0],
  &_EnrolStaff_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t EnrolStaff_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EnrolStaff_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Response__get_type_hash,
  &acare_msgs__srv__EnrolStaff_Response__get_type_description,
  &acare_msgs__srv__EnrolStaff_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace acare_msgs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, acare_msgs, srv, EnrolStaff_Response)() {
  return &::acare_msgs::srv::rosidl_typesupport_c::EnrolStaff_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__struct.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__type_support.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace acare_msgs
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _EnrolStaff_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EnrolStaff_Event_type_support_ids_t;

static const _EnrolStaff_Event_type_support_ids_t _EnrolStaff_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _EnrolStaff_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EnrolStaff_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EnrolStaff_Event_type_support_symbol_names_t _EnrolStaff_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, srv, EnrolStaff_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff_Event)),
  }
};

typedef struct _EnrolStaff_Event_type_support_data_t
{
  void * data[2];
} _EnrolStaff_Event_type_support_data_t;

static _EnrolStaff_Event_type_support_data_t _EnrolStaff_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EnrolStaff_Event_message_typesupport_map = {
  2,
  "acare_msgs",
  &_EnrolStaff_Event_message_typesupport_ids.typesupport_identifier[0],
  &_EnrolStaff_Event_message_typesupport_symbol_names.symbol_name[0],
  &_EnrolStaff_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t EnrolStaff_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EnrolStaff_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &acare_msgs__srv__EnrolStaff_Event__get_type_hash,
  &acare_msgs__srv__EnrolStaff_Event__get_type_description,
  &acare_msgs__srv__EnrolStaff_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace acare_msgs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, acare_msgs, srv, EnrolStaff_Event)() {
  return &::acare_msgs::srv::rosidl_typesupport_c::EnrolStaff_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace acare_msgs
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _EnrolStaff_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _EnrolStaff_type_support_ids_t;

static const _EnrolStaff_type_support_ids_t _EnrolStaff_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _EnrolStaff_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _EnrolStaff_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _EnrolStaff_type_support_symbol_names_t _EnrolStaff_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, acare_msgs, srv, EnrolStaff)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, acare_msgs, srv, EnrolStaff)),
  }
};

typedef struct _EnrolStaff_type_support_data_t
{
  void * data[2];
} _EnrolStaff_type_support_data_t;

static _EnrolStaff_type_support_data_t _EnrolStaff_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _EnrolStaff_service_typesupport_map = {
  2,
  "acare_msgs",
  &_EnrolStaff_service_typesupport_ids.typesupport_identifier[0],
  &_EnrolStaff_service_typesupport_symbol_names.symbol_name[0],
  &_EnrolStaff_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t EnrolStaff_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_EnrolStaff_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &EnrolStaff_Request_message_type_support_handle,
  &EnrolStaff_Response_message_type_support_handle,
  &EnrolStaff_Event_message_type_support_handle,
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

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace acare_msgs

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, acare_msgs, srv, EnrolStaff)() {
  return &::acare_msgs::srv::rosidl_typesupport_c::EnrolStaff_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

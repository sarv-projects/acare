// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/LogEvent.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/log_event__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__LogEvent__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xf6, 0x56, 0x47, 0xbe, 0x1d, 0xcc, 0x58, 0x11,
      0xb3, 0x87, 0x3a, 0x53, 0x58, 0x4e, 0xfe, 0x57,
      0x9d, 0xf9, 0xcd, 0xc3, 0x3d, 0x69, 0x2d, 0xef,
      0x8e, 0xbd, 0xd9, 0xaf, 0xa2, 0xa1, 0xed, 0xe4,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__LogEvent__TYPE_NAME[] = "acare_msgs/msg/LogEvent";

// Define type names, field names, and default values
static char acare_msgs__msg__LogEvent__FIELD_NAME__event_type[] = "event_type";
static char acare_msgs__msg__LogEvent__FIELD_NAME__user_id[] = "user_id";
static char acare_msgs__msg__LogEvent__FIELD_NAME__tool[] = "tool";
static char acare_msgs__msg__LogEvent__FIELD_NAME__state[] = "state";
static char acare_msgs__msg__LogEvent__FIELD_NAME__description[] = "description";
static char acare_msgs__msg__LogEvent__FIELD_NAME__timestamp[] = "timestamp";
static char acare_msgs__msg__LogEvent__FIELD_NAME__voice_e2e_ms[] = "voice_e2e_ms";
static char acare_msgs__msg__LogEvent__FIELD_NAME__vision_search_ms[] = "vision_search_ms";
static char acare_msgs__msg__LogEvent__FIELD_NAME__motion_ms[] = "motion_ms";
static char acare_msgs__msg__LogEvent__FIELD_NAME__total_task_ms[] = "total_task_ms";
static char acare_msgs__msg__LogEvent__FIELD_NAME__safety_severity[] = "safety_severity";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__LogEvent__FIELDS[] = {
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__event_type, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__user_id, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__tool, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__state, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__description, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__timestamp, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__voice_e2e_ms, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__vision_search_ms, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__motion_ms, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__total_task_ms, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__LogEvent__FIELD_NAME__safety_severity, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__msg__LogEvent__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__LogEvent__TYPE_NAME, 23, 23},
      {acare_msgs__msg__LogEvent__FIELDS, 11, 11},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string event_type\n"
  "string user_id\n"
  "string tool\n"
  "string state\n"
  "string description\n"
  "int64 timestamp\n"
  "int64 voice_e2e_ms\n"
  "int64 vision_search_ms\n"
  "int64 motion_ms\n"
  "int64 total_task_ms\n"
  "string safety_severity";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__LogEvent__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__LogEvent__TYPE_NAME, 23, 23},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 194, 194},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__LogEvent__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__LogEvent__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

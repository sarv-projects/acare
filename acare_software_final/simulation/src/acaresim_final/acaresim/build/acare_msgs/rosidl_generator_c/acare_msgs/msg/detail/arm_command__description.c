// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/arm_command__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__ArmCommand__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x28, 0x5d, 0xc9, 0x10, 0xf8, 0xb8, 0x59, 0x58,
      0xc2, 0x2c, 0x8b, 0x7e, 0x77, 0x9c, 0xc6, 0x8d,
      0xaa, 0x18, 0x13, 0x58, 0x7e, 0x6b, 0x41, 0xcd,
      0x96, 0x17, 0x20, 0x0c, 0x17, 0x90, 0x4c, 0xe8,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__ArmCommand__TYPE_NAME[] = "acare_msgs/msg/ArmCommand";

// Define type names, field names, and default values
static char acare_msgs__msg__ArmCommand__FIELD_NAME__command[] = "command";
static char acare_msgs__msg__ArmCommand__FIELD_NAME__joint_angles[] = "joint_angles";
static char acare_msgs__msg__ArmCommand__FIELD_NAME__velocity_scale[] = "velocity_scale";
static char acare_msgs__msg__ArmCommand__FIELD_NAME__accel_limit[] = "accel_limit";
static char acare_msgs__msg__ArmCommand__FIELD_NAME__blocking[] = "blocking";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__ArmCommand__FIELDS[] = {
  {
    {acare_msgs__msg__ArmCommand__FIELD_NAME__command, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ArmCommand__FIELD_NAME__joint_angles, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ArmCommand__FIELD_NAME__velocity_scale, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ArmCommand__FIELD_NAME__accel_limit, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__ArmCommand__FIELD_NAME__blocking, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__msg__ArmCommand__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__ArmCommand__TYPE_NAME, 25, 25},
      {acare_msgs__msg__ArmCommand__FIELDS, 5, 5},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string command\n"
  "float32[] joint_angles\n"
  "float32 velocity_scale\n"
  "float32 accel_limit\n"
  "bool blocking";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__ArmCommand__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__ArmCommand__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 95, 95},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__ArmCommand__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__ArmCommand__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

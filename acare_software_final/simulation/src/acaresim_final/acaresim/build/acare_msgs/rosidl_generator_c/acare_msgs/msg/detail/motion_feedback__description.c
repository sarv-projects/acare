// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice

#include "acare_msgs/msg/detail/motion_feedback__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__msg__MotionFeedback__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x24, 0xb8, 0x65, 0x2e, 0x3b, 0x6b, 0xb8, 0xcd,
      0xca, 0x4d, 0xb8, 0x44, 0xbf, 0x71, 0x67, 0x5d,
      0x13, 0xed, 0x82, 0xf3, 0xfa, 0xc1, 0x86, 0x36,
      0x65, 0xe7, 0xce, 0x89, 0xd4, 0x89, 0x56, 0xeb,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char acare_msgs__msg__MotionFeedback__TYPE_NAME[] = "acare_msgs/msg/MotionFeedback";

// Define type names, field names, and default values
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__success[] = "success";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__phase[] = "phase";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__error[] = "error";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__joint_positions[] = "joint_positions";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__joint_velocities[] = "joint_velocities";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__joint_currents[] = "joint_currents";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__temperatures[] = "temperatures";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__gripper_force[] = "gripper_force";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__imu_roll[] = "imu_roll";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__imu_pitch[] = "imu_pitch";
static char acare_msgs__msg__MotionFeedback__FIELD_NAME__imu_yaw[] = "imu_yaw";

static rosidl_runtime_c__type_description__Field acare_msgs__msg__MotionFeedback__FIELDS[] = {
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__success, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__phase, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__error, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__joint_positions, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__joint_velocities, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__joint_currents, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__temperatures, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__gripper_force, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__imu_roll, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__imu_pitch, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {acare_msgs__msg__MotionFeedback__FIELD_NAME__imu_yaw, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__msg__MotionFeedback__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {acare_msgs__msg__MotionFeedback__TYPE_NAME, 29, 29},
      {acare_msgs__msg__MotionFeedback__FIELDS, 11, 11},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "bool success\n"
  "string phase\n"
  "string error\n"
  "float32[] joint_positions\n"
  "float32[] joint_velocities\n"
  "float32[] joint_currents\n"
  "float32[] temperatures\n"
  "float32 gripper_force\n"
  "float32 imu_roll\n"
  "float32 imu_pitch\n"
  "float32 imu_yaw";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__msg__MotionFeedback__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {acare_msgs__msg__MotionFeedback__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 213, 213},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__msg__MotionFeedback__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *acare_msgs__msg__MotionFeedback__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

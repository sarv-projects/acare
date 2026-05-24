// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/MotionFeedback.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/motion_feedback__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `phase`
// Member `error`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_positions`
// Member `joint_velocities`
// Member `joint_currents`
// Member `temperatures`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
acare_msgs__msg__MotionFeedback__init(acare_msgs__msg__MotionFeedback * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // phase
  if (!rosidl_runtime_c__String__init(&msg->phase)) {
    acare_msgs__msg__MotionFeedback__fini(msg);
    return false;
  }
  // error
  if (!rosidl_runtime_c__String__init(&msg->error)) {
    acare_msgs__msg__MotionFeedback__fini(msg);
    return false;
  }
  // joint_positions
  if (!rosidl_runtime_c__float__Sequence__init(&msg->joint_positions, 0)) {
    acare_msgs__msg__MotionFeedback__fini(msg);
    return false;
  }
  // joint_velocities
  if (!rosidl_runtime_c__float__Sequence__init(&msg->joint_velocities, 0)) {
    acare_msgs__msg__MotionFeedback__fini(msg);
    return false;
  }
  // joint_currents
  if (!rosidl_runtime_c__float__Sequence__init(&msg->joint_currents, 0)) {
    acare_msgs__msg__MotionFeedback__fini(msg);
    return false;
  }
  // temperatures
  if (!rosidl_runtime_c__float__Sequence__init(&msg->temperatures, 0)) {
    acare_msgs__msg__MotionFeedback__fini(msg);
    return false;
  }
  // gripper_force
  // imu_roll
  // imu_pitch
  // imu_yaw
  return true;
}

void
acare_msgs__msg__MotionFeedback__fini(acare_msgs__msg__MotionFeedback * msg)
{
  if (!msg) {
    return;
  }
  // success
  // phase
  rosidl_runtime_c__String__fini(&msg->phase);
  // error
  rosidl_runtime_c__String__fini(&msg->error);
  // joint_positions
  rosidl_runtime_c__float__Sequence__fini(&msg->joint_positions);
  // joint_velocities
  rosidl_runtime_c__float__Sequence__fini(&msg->joint_velocities);
  // joint_currents
  rosidl_runtime_c__float__Sequence__fini(&msg->joint_currents);
  // temperatures
  rosidl_runtime_c__float__Sequence__fini(&msg->temperatures);
  // gripper_force
  // imu_roll
  // imu_pitch
  // imu_yaw
}

bool
acare_msgs__msg__MotionFeedback__are_equal(const acare_msgs__msg__MotionFeedback * lhs, const acare_msgs__msg__MotionFeedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // phase
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->phase), &(rhs->phase)))
  {
    return false;
  }
  // error
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error), &(rhs->error)))
  {
    return false;
  }
  // joint_positions
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->joint_positions), &(rhs->joint_positions)))
  {
    return false;
  }
  // joint_velocities
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->joint_velocities), &(rhs->joint_velocities)))
  {
    return false;
  }
  // joint_currents
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->joint_currents), &(rhs->joint_currents)))
  {
    return false;
  }
  // temperatures
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->temperatures), &(rhs->temperatures)))
  {
    return false;
  }
  // gripper_force
  if (lhs->gripper_force != rhs->gripper_force) {
    return false;
  }
  // imu_roll
  if (lhs->imu_roll != rhs->imu_roll) {
    return false;
  }
  // imu_pitch
  if (lhs->imu_pitch != rhs->imu_pitch) {
    return false;
  }
  // imu_yaw
  if (lhs->imu_yaw != rhs->imu_yaw) {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__MotionFeedback__copy(
  const acare_msgs__msg__MotionFeedback * input,
  acare_msgs__msg__MotionFeedback * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // phase
  if (!rosidl_runtime_c__String__copy(
      &(input->phase), &(output->phase)))
  {
    return false;
  }
  // error
  if (!rosidl_runtime_c__String__copy(
      &(input->error), &(output->error)))
  {
    return false;
  }
  // joint_positions
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->joint_positions), &(output->joint_positions)))
  {
    return false;
  }
  // joint_velocities
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->joint_velocities), &(output->joint_velocities)))
  {
    return false;
  }
  // joint_currents
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->joint_currents), &(output->joint_currents)))
  {
    return false;
  }
  // temperatures
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->temperatures), &(output->temperatures)))
  {
    return false;
  }
  // gripper_force
  output->gripper_force = input->gripper_force;
  // imu_roll
  output->imu_roll = input->imu_roll;
  // imu_pitch
  output->imu_pitch = input->imu_pitch;
  // imu_yaw
  output->imu_yaw = input->imu_yaw;
  return true;
}

acare_msgs__msg__MotionFeedback *
acare_msgs__msg__MotionFeedback__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__MotionFeedback * msg = (acare_msgs__msg__MotionFeedback *)allocator.allocate(sizeof(acare_msgs__msg__MotionFeedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__MotionFeedback));
  bool success = acare_msgs__msg__MotionFeedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__MotionFeedback__destroy(acare_msgs__msg__MotionFeedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__MotionFeedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__MotionFeedback__Sequence__init(acare_msgs__msg__MotionFeedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__MotionFeedback * data = NULL;

  if (size) {
    data = (acare_msgs__msg__MotionFeedback *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__MotionFeedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__MotionFeedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__MotionFeedback__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
acare_msgs__msg__MotionFeedback__Sequence__fini(acare_msgs__msg__MotionFeedback__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      acare_msgs__msg__MotionFeedback__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

acare_msgs__msg__MotionFeedback__Sequence *
acare_msgs__msg__MotionFeedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__MotionFeedback__Sequence * array = (acare_msgs__msg__MotionFeedback__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__MotionFeedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__MotionFeedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__MotionFeedback__Sequence__destroy(acare_msgs__msg__MotionFeedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__MotionFeedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__MotionFeedback__Sequence__are_equal(const acare_msgs__msg__MotionFeedback__Sequence * lhs, const acare_msgs__msg__MotionFeedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__MotionFeedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__MotionFeedback__Sequence__copy(
  const acare_msgs__msg__MotionFeedback__Sequence * input,
  acare_msgs__msg__MotionFeedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__MotionFeedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__MotionFeedback * data =
      (acare_msgs__msg__MotionFeedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__MotionFeedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__MotionFeedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__MotionFeedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

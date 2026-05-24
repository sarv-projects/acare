// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/ArmCommand.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/arm_command__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `command`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_angles`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
acare_msgs__msg__ArmCommand__init(acare_msgs__msg__ArmCommand * msg)
{
  if (!msg) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__init(&msg->command)) {
    acare_msgs__msg__ArmCommand__fini(msg);
    return false;
  }
  // joint_angles
  if (!rosidl_runtime_c__float__Sequence__init(&msg->joint_angles, 0)) {
    acare_msgs__msg__ArmCommand__fini(msg);
    return false;
  }
  // velocity_scale
  // accel_limit
  // blocking
  return true;
}

void
acare_msgs__msg__ArmCommand__fini(acare_msgs__msg__ArmCommand * msg)
{
  if (!msg) {
    return;
  }
  // command
  rosidl_runtime_c__String__fini(&msg->command);
  // joint_angles
  rosidl_runtime_c__float__Sequence__fini(&msg->joint_angles);
  // velocity_scale
  // accel_limit
  // blocking
}

bool
acare_msgs__msg__ArmCommand__are_equal(const acare_msgs__msg__ArmCommand * lhs, const acare_msgs__msg__ArmCommand * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->command), &(rhs->command)))
  {
    return false;
  }
  // joint_angles
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->joint_angles), &(rhs->joint_angles)))
  {
    return false;
  }
  // velocity_scale
  if (lhs->velocity_scale != rhs->velocity_scale) {
    return false;
  }
  // accel_limit
  if (lhs->accel_limit != rhs->accel_limit) {
    return false;
  }
  // blocking
  if (lhs->blocking != rhs->blocking) {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__ArmCommand__copy(
  const acare_msgs__msg__ArmCommand * input,
  acare_msgs__msg__ArmCommand * output)
{
  if (!input || !output) {
    return false;
  }
  // command
  if (!rosidl_runtime_c__String__copy(
      &(input->command), &(output->command)))
  {
    return false;
  }
  // joint_angles
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->joint_angles), &(output->joint_angles)))
  {
    return false;
  }
  // velocity_scale
  output->velocity_scale = input->velocity_scale;
  // accel_limit
  output->accel_limit = input->accel_limit;
  // blocking
  output->blocking = input->blocking;
  return true;
}

acare_msgs__msg__ArmCommand *
acare_msgs__msg__ArmCommand__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__ArmCommand * msg = (acare_msgs__msg__ArmCommand *)allocator.allocate(sizeof(acare_msgs__msg__ArmCommand), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__ArmCommand));
  bool success = acare_msgs__msg__ArmCommand__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__ArmCommand__destroy(acare_msgs__msg__ArmCommand * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__ArmCommand__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__ArmCommand__Sequence__init(acare_msgs__msg__ArmCommand__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__ArmCommand * data = NULL;

  if (size) {
    data = (acare_msgs__msg__ArmCommand *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__ArmCommand), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__ArmCommand__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__ArmCommand__fini(&data[i - 1]);
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
acare_msgs__msg__ArmCommand__Sequence__fini(acare_msgs__msg__ArmCommand__Sequence * array)
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
      acare_msgs__msg__ArmCommand__fini(&array->data[i]);
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

acare_msgs__msg__ArmCommand__Sequence *
acare_msgs__msg__ArmCommand__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__ArmCommand__Sequence * array = (acare_msgs__msg__ArmCommand__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__ArmCommand__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__ArmCommand__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__ArmCommand__Sequence__destroy(acare_msgs__msg__ArmCommand__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__ArmCommand__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__ArmCommand__Sequence__are_equal(const acare_msgs__msg__ArmCommand__Sequence * lhs, const acare_msgs__msg__ArmCommand__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__ArmCommand__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__ArmCommand__Sequence__copy(
  const acare_msgs__msg__ArmCommand__Sequence * input,
  acare_msgs__msg__ArmCommand__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__ArmCommand);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__ArmCommand * data =
      (acare_msgs__msg__ArmCommand *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__ArmCommand__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__ArmCommand__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__ArmCommand__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

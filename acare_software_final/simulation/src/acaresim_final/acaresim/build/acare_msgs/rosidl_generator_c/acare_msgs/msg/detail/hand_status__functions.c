// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/HandStatus.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/hand_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
acare_msgs__msg__HandStatus__init(acare_msgs__msg__HandStatus * msg)
{
  if (!msg) {
    return false;
  }
  // hand_detected
  // is_open
  // palm_up
  // x
  // y
  // z
  // confidence
  return true;
}

void
acare_msgs__msg__HandStatus__fini(acare_msgs__msg__HandStatus * msg)
{
  if (!msg) {
    return;
  }
  // hand_detected
  // is_open
  // palm_up
  // x
  // y
  // z
  // confidence
}

bool
acare_msgs__msg__HandStatus__are_equal(const acare_msgs__msg__HandStatus * lhs, const acare_msgs__msg__HandStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // hand_detected
  if (lhs->hand_detected != rhs->hand_detected) {
    return false;
  }
  // is_open
  if (lhs->is_open != rhs->is_open) {
    return false;
  }
  // palm_up
  if (lhs->palm_up != rhs->palm_up) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__HandStatus__copy(
  const acare_msgs__msg__HandStatus * input,
  acare_msgs__msg__HandStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // hand_detected
  output->hand_detected = input->hand_detected;
  // is_open
  output->is_open = input->is_open;
  // palm_up
  output->palm_up = input->palm_up;
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // confidence
  output->confidence = input->confidence;
  return true;
}

acare_msgs__msg__HandStatus *
acare_msgs__msg__HandStatus__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__HandStatus * msg = (acare_msgs__msg__HandStatus *)allocator.allocate(sizeof(acare_msgs__msg__HandStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__HandStatus));
  bool success = acare_msgs__msg__HandStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__HandStatus__destroy(acare_msgs__msg__HandStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__HandStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__HandStatus__Sequence__init(acare_msgs__msg__HandStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__HandStatus * data = NULL;

  if (size) {
    data = (acare_msgs__msg__HandStatus *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__HandStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__HandStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__HandStatus__fini(&data[i - 1]);
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
acare_msgs__msg__HandStatus__Sequence__fini(acare_msgs__msg__HandStatus__Sequence * array)
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
      acare_msgs__msg__HandStatus__fini(&array->data[i]);
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

acare_msgs__msg__HandStatus__Sequence *
acare_msgs__msg__HandStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__HandStatus__Sequence * array = (acare_msgs__msg__HandStatus__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__HandStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__HandStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__HandStatus__Sequence__destroy(acare_msgs__msg__HandStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__HandStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__HandStatus__Sequence__are_equal(const acare_msgs__msg__HandStatus__Sequence * lhs, const acare_msgs__msg__HandStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__HandStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__HandStatus__Sequence__copy(
  const acare_msgs__msg__HandStatus__Sequence * input,
  acare_msgs__msg__HandStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__HandStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__HandStatus * data =
      (acare_msgs__msg__HandStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__HandStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__HandStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__HandStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

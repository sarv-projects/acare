// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:msg/VisionSearchRequest.idl
// generated code does not contain a copyright notice
#include "acare_msgs/msg/detail/vision_search_request__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `tool`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__msg__VisionSearchRequest__init(acare_msgs__msg__VisionSearchRequest * msg)
{
  if (!msg) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__init(&msg->tool)) {
    acare_msgs__msg__VisionSearchRequest__fini(msg);
    return false;
  }
  return true;
}

void
acare_msgs__msg__VisionSearchRequest__fini(acare_msgs__msg__VisionSearchRequest * msg)
{
  if (!msg) {
    return;
  }
  // tool
  rosidl_runtime_c__String__fini(&msg->tool);
}

bool
acare_msgs__msg__VisionSearchRequest__are_equal(const acare_msgs__msg__VisionSearchRequest * lhs, const acare_msgs__msg__VisionSearchRequest * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->tool), &(rhs->tool)))
  {
    return false;
  }
  return true;
}

bool
acare_msgs__msg__VisionSearchRequest__copy(
  const acare_msgs__msg__VisionSearchRequest * input,
  acare_msgs__msg__VisionSearchRequest * output)
{
  if (!input || !output) {
    return false;
  }
  // tool
  if (!rosidl_runtime_c__String__copy(
      &(input->tool), &(output->tool)))
  {
    return false;
  }
  return true;
}

acare_msgs__msg__VisionSearchRequest *
acare_msgs__msg__VisionSearchRequest__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__VisionSearchRequest * msg = (acare_msgs__msg__VisionSearchRequest *)allocator.allocate(sizeof(acare_msgs__msg__VisionSearchRequest), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__msg__VisionSearchRequest));
  bool success = acare_msgs__msg__VisionSearchRequest__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__msg__VisionSearchRequest__destroy(acare_msgs__msg__VisionSearchRequest * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__msg__VisionSearchRequest__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__msg__VisionSearchRequest__Sequence__init(acare_msgs__msg__VisionSearchRequest__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__VisionSearchRequest * data = NULL;

  if (size) {
    data = (acare_msgs__msg__VisionSearchRequest *)allocator.zero_allocate(size, sizeof(acare_msgs__msg__VisionSearchRequest), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__msg__VisionSearchRequest__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__msg__VisionSearchRequest__fini(&data[i - 1]);
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
acare_msgs__msg__VisionSearchRequest__Sequence__fini(acare_msgs__msg__VisionSearchRequest__Sequence * array)
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
      acare_msgs__msg__VisionSearchRequest__fini(&array->data[i]);
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

acare_msgs__msg__VisionSearchRequest__Sequence *
acare_msgs__msg__VisionSearchRequest__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__msg__VisionSearchRequest__Sequence * array = (acare_msgs__msg__VisionSearchRequest__Sequence *)allocator.allocate(sizeof(acare_msgs__msg__VisionSearchRequest__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__msg__VisionSearchRequest__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__msg__VisionSearchRequest__Sequence__destroy(acare_msgs__msg__VisionSearchRequest__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__msg__VisionSearchRequest__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__msg__VisionSearchRequest__Sequence__are_equal(const acare_msgs__msg__VisionSearchRequest__Sequence * lhs, const acare_msgs__msg__VisionSearchRequest__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__msg__VisionSearchRequest__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__msg__VisionSearchRequest__Sequence__copy(
  const acare_msgs__msg__VisionSearchRequest__Sequence * input,
  acare_msgs__msg__VisionSearchRequest__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__msg__VisionSearchRequest);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__msg__VisionSearchRequest * data =
      (acare_msgs__msg__VisionSearchRequest *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__msg__VisionSearchRequest__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__msg__VisionSearchRequest__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__msg__VisionSearchRequest__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

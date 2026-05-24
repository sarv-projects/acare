// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice
#include "acare_msgs/srv/detail/enrol_staff__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `name`
// Member `role`
#include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__srv__EnrolStaff_Request__init(acare_msgs__srv__EnrolStaff_Request * msg)
{
  if (!msg) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    acare_msgs__srv__EnrolStaff_Request__fini(msg);
    return false;
  }
  // role
  if (!rosidl_runtime_c__String__init(&msg->role)) {
    acare_msgs__srv__EnrolStaff_Request__fini(msg);
    return false;
  }
  return true;
}

void
acare_msgs__srv__EnrolStaff_Request__fini(acare_msgs__srv__EnrolStaff_Request * msg)
{
  if (!msg) {
    return;
  }
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // role
  rosidl_runtime_c__String__fini(&msg->role);
}

bool
acare_msgs__srv__EnrolStaff_Request__are_equal(const acare_msgs__srv__EnrolStaff_Request * lhs, const acare_msgs__srv__EnrolStaff_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // role
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->role), &(rhs->role)))
  {
    return false;
  }
  return true;
}

bool
acare_msgs__srv__EnrolStaff_Request__copy(
  const acare_msgs__srv__EnrolStaff_Request * input,
  acare_msgs__srv__EnrolStaff_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // role
  if (!rosidl_runtime_c__String__copy(
      &(input->role), &(output->role)))
  {
    return false;
  }
  return true;
}

acare_msgs__srv__EnrolStaff_Request *
acare_msgs__srv__EnrolStaff_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Request * msg = (acare_msgs__srv__EnrolStaff_Request *)allocator.allocate(sizeof(acare_msgs__srv__EnrolStaff_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__srv__EnrolStaff_Request));
  bool success = acare_msgs__srv__EnrolStaff_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__srv__EnrolStaff_Request__destroy(acare_msgs__srv__EnrolStaff_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__srv__EnrolStaff_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__srv__EnrolStaff_Request__Sequence__init(acare_msgs__srv__EnrolStaff_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Request * data = NULL;

  if (size) {
    data = (acare_msgs__srv__EnrolStaff_Request *)allocator.zero_allocate(size, sizeof(acare_msgs__srv__EnrolStaff_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__srv__EnrolStaff_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__srv__EnrolStaff_Request__fini(&data[i - 1]);
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
acare_msgs__srv__EnrolStaff_Request__Sequence__fini(acare_msgs__srv__EnrolStaff_Request__Sequence * array)
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
      acare_msgs__srv__EnrolStaff_Request__fini(&array->data[i]);
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

acare_msgs__srv__EnrolStaff_Request__Sequence *
acare_msgs__srv__EnrolStaff_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Request__Sequence * array = (acare_msgs__srv__EnrolStaff_Request__Sequence *)allocator.allocate(sizeof(acare_msgs__srv__EnrolStaff_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__srv__EnrolStaff_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__srv__EnrolStaff_Request__Sequence__destroy(acare_msgs__srv__EnrolStaff_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__srv__EnrolStaff_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__srv__EnrolStaff_Request__Sequence__are_equal(const acare_msgs__srv__EnrolStaff_Request__Sequence * lhs, const acare_msgs__srv__EnrolStaff_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__srv__EnrolStaff_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__srv__EnrolStaff_Request__Sequence__copy(
  const acare_msgs__srv__EnrolStaff_Request__Sequence * input,
  acare_msgs__srv__EnrolStaff_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__srv__EnrolStaff_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__srv__EnrolStaff_Request * data =
      (acare_msgs__srv__EnrolStaff_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__srv__EnrolStaff_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__srv__EnrolStaff_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__srv__EnrolStaff_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `staff_id`
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
acare_msgs__srv__EnrolStaff_Response__init(acare_msgs__srv__EnrolStaff_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // staff_id
  if (!rosidl_runtime_c__String__init(&msg->staff_id)) {
    acare_msgs__srv__EnrolStaff_Response__fini(msg);
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    acare_msgs__srv__EnrolStaff_Response__fini(msg);
    return false;
  }
  return true;
}

void
acare_msgs__srv__EnrolStaff_Response__fini(acare_msgs__srv__EnrolStaff_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // staff_id
  rosidl_runtime_c__String__fini(&msg->staff_id);
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
acare_msgs__srv__EnrolStaff_Response__are_equal(const acare_msgs__srv__EnrolStaff_Response * lhs, const acare_msgs__srv__EnrolStaff_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // staff_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->staff_id), &(rhs->staff_id)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
acare_msgs__srv__EnrolStaff_Response__copy(
  const acare_msgs__srv__EnrolStaff_Response * input,
  acare_msgs__srv__EnrolStaff_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // staff_id
  if (!rosidl_runtime_c__String__copy(
      &(input->staff_id), &(output->staff_id)))
  {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

acare_msgs__srv__EnrolStaff_Response *
acare_msgs__srv__EnrolStaff_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Response * msg = (acare_msgs__srv__EnrolStaff_Response *)allocator.allocate(sizeof(acare_msgs__srv__EnrolStaff_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__srv__EnrolStaff_Response));
  bool success = acare_msgs__srv__EnrolStaff_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__srv__EnrolStaff_Response__destroy(acare_msgs__srv__EnrolStaff_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__srv__EnrolStaff_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__srv__EnrolStaff_Response__Sequence__init(acare_msgs__srv__EnrolStaff_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Response * data = NULL;

  if (size) {
    data = (acare_msgs__srv__EnrolStaff_Response *)allocator.zero_allocate(size, sizeof(acare_msgs__srv__EnrolStaff_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__srv__EnrolStaff_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__srv__EnrolStaff_Response__fini(&data[i - 1]);
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
acare_msgs__srv__EnrolStaff_Response__Sequence__fini(acare_msgs__srv__EnrolStaff_Response__Sequence * array)
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
      acare_msgs__srv__EnrolStaff_Response__fini(&array->data[i]);
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

acare_msgs__srv__EnrolStaff_Response__Sequence *
acare_msgs__srv__EnrolStaff_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Response__Sequence * array = (acare_msgs__srv__EnrolStaff_Response__Sequence *)allocator.allocate(sizeof(acare_msgs__srv__EnrolStaff_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__srv__EnrolStaff_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__srv__EnrolStaff_Response__Sequence__destroy(acare_msgs__srv__EnrolStaff_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__srv__EnrolStaff_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__srv__EnrolStaff_Response__Sequence__are_equal(const acare_msgs__srv__EnrolStaff_Response__Sequence * lhs, const acare_msgs__srv__EnrolStaff_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__srv__EnrolStaff_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__srv__EnrolStaff_Response__Sequence__copy(
  const acare_msgs__srv__EnrolStaff_Response__Sequence * input,
  acare_msgs__srv__EnrolStaff_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__srv__EnrolStaff_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__srv__EnrolStaff_Response * data =
      (acare_msgs__srv__EnrolStaff_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__srv__EnrolStaff_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__srv__EnrolStaff_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__srv__EnrolStaff_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "acare_msgs/srv/detail/enrol_staff__functions.h"

bool
acare_msgs__srv__EnrolStaff_Event__init(acare_msgs__srv__EnrolStaff_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    acare_msgs__srv__EnrolStaff_Event__fini(msg);
    return false;
  }
  // request
  if (!acare_msgs__srv__EnrolStaff_Request__Sequence__init(&msg->request, 0)) {
    acare_msgs__srv__EnrolStaff_Event__fini(msg);
    return false;
  }
  // response
  if (!acare_msgs__srv__EnrolStaff_Response__Sequence__init(&msg->response, 0)) {
    acare_msgs__srv__EnrolStaff_Event__fini(msg);
    return false;
  }
  return true;
}

void
acare_msgs__srv__EnrolStaff_Event__fini(acare_msgs__srv__EnrolStaff_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  acare_msgs__srv__EnrolStaff_Request__Sequence__fini(&msg->request);
  // response
  acare_msgs__srv__EnrolStaff_Response__Sequence__fini(&msg->response);
}

bool
acare_msgs__srv__EnrolStaff_Event__are_equal(const acare_msgs__srv__EnrolStaff_Event * lhs, const acare_msgs__srv__EnrolStaff_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!acare_msgs__srv__EnrolStaff_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!acare_msgs__srv__EnrolStaff_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
acare_msgs__srv__EnrolStaff_Event__copy(
  const acare_msgs__srv__EnrolStaff_Event * input,
  acare_msgs__srv__EnrolStaff_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!acare_msgs__srv__EnrolStaff_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!acare_msgs__srv__EnrolStaff_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

acare_msgs__srv__EnrolStaff_Event *
acare_msgs__srv__EnrolStaff_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Event * msg = (acare_msgs__srv__EnrolStaff_Event *)allocator.allocate(sizeof(acare_msgs__srv__EnrolStaff_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(acare_msgs__srv__EnrolStaff_Event));
  bool success = acare_msgs__srv__EnrolStaff_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
acare_msgs__srv__EnrolStaff_Event__destroy(acare_msgs__srv__EnrolStaff_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    acare_msgs__srv__EnrolStaff_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
acare_msgs__srv__EnrolStaff_Event__Sequence__init(acare_msgs__srv__EnrolStaff_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Event * data = NULL;

  if (size) {
    data = (acare_msgs__srv__EnrolStaff_Event *)allocator.zero_allocate(size, sizeof(acare_msgs__srv__EnrolStaff_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = acare_msgs__srv__EnrolStaff_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        acare_msgs__srv__EnrolStaff_Event__fini(&data[i - 1]);
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
acare_msgs__srv__EnrolStaff_Event__Sequence__fini(acare_msgs__srv__EnrolStaff_Event__Sequence * array)
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
      acare_msgs__srv__EnrolStaff_Event__fini(&array->data[i]);
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

acare_msgs__srv__EnrolStaff_Event__Sequence *
acare_msgs__srv__EnrolStaff_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  acare_msgs__srv__EnrolStaff_Event__Sequence * array = (acare_msgs__srv__EnrolStaff_Event__Sequence *)allocator.allocate(sizeof(acare_msgs__srv__EnrolStaff_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = acare_msgs__srv__EnrolStaff_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
acare_msgs__srv__EnrolStaff_Event__Sequence__destroy(acare_msgs__srv__EnrolStaff_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    acare_msgs__srv__EnrolStaff_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
acare_msgs__srv__EnrolStaff_Event__Sequence__are_equal(const acare_msgs__srv__EnrolStaff_Event__Sequence * lhs, const acare_msgs__srv__EnrolStaff_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!acare_msgs__srv__EnrolStaff_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
acare_msgs__srv__EnrolStaff_Event__Sequence__copy(
  const acare_msgs__srv__EnrolStaff_Event__Sequence * input,
  acare_msgs__srv__EnrolStaff_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(acare_msgs__srv__EnrolStaff_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    acare_msgs__srv__EnrolStaff_Event * data =
      (acare_msgs__srv__EnrolStaff_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!acare_msgs__srv__EnrolStaff_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          acare_msgs__srv__EnrolStaff_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!acare_msgs__srv__EnrolStaff_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

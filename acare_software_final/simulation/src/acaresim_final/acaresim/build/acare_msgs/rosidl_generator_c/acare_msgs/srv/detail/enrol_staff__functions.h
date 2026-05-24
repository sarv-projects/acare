// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from acare_msgs:srv/EnrolStaff.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/srv/enrol_staff.h"


#ifndef ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__FUNCTIONS_H_
#define ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "acare_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "acare_msgs/srv/detail/enrol_staff__struct.h"

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__srv__EnrolStaff__get_type_hash(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__srv__EnrolStaff__get_type_description(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__srv__EnrolStaff__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__srv__EnrolStaff__get_type_description_sources(
  const rosidl_service_type_support_t * type_support);

/// Initialize srv/EnrolStaff message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * acare_msgs__srv__EnrolStaff_Request
 * )) before or use
 * acare_msgs__srv__EnrolStaff_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Request__init(acare_msgs__srv__EnrolStaff_Request * msg);

/// Finalize srv/EnrolStaff message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Request__fini(acare_msgs__srv__EnrolStaff_Request * msg);

/// Create srv/EnrolStaff message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * acare_msgs__srv__EnrolStaff_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
acare_msgs__srv__EnrolStaff_Request *
acare_msgs__srv__EnrolStaff_Request__create(void);

/// Destroy srv/EnrolStaff message.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Request__destroy(acare_msgs__srv__EnrolStaff_Request * msg);

/// Check for srv/EnrolStaff message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Request__are_equal(const acare_msgs__srv__EnrolStaff_Request * lhs, const acare_msgs__srv__EnrolStaff_Request * rhs);

/// Copy a srv/EnrolStaff message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Request__copy(
  const acare_msgs__srv__EnrolStaff_Request * input,
  acare_msgs__srv__EnrolStaff_Request * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__srv__EnrolStaff_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__srv__EnrolStaff_Request__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__srv__EnrolStaff_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__srv__EnrolStaff_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/EnrolStaff messages.
/**
 * It allocates the memory for the number of elements and calls
 * acare_msgs__srv__EnrolStaff_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Request__Sequence__init(acare_msgs__srv__EnrolStaff_Request__Sequence * array, size_t size);

/// Finalize array of srv/EnrolStaff messages.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Request__Sequence__fini(acare_msgs__srv__EnrolStaff_Request__Sequence * array);

/// Create array of srv/EnrolStaff messages.
/**
 * It allocates the memory for the array and calls
 * acare_msgs__srv__EnrolStaff_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
acare_msgs__srv__EnrolStaff_Request__Sequence *
acare_msgs__srv__EnrolStaff_Request__Sequence__create(size_t size);

/// Destroy array of srv/EnrolStaff messages.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Request__Sequence__destroy(acare_msgs__srv__EnrolStaff_Request__Sequence * array);

/// Check for srv/EnrolStaff message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Request__Sequence__are_equal(const acare_msgs__srv__EnrolStaff_Request__Sequence * lhs, const acare_msgs__srv__EnrolStaff_Request__Sequence * rhs);

/// Copy an array of srv/EnrolStaff messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Request__Sequence__copy(
  const acare_msgs__srv__EnrolStaff_Request__Sequence * input,
  acare_msgs__srv__EnrolStaff_Request__Sequence * output);

/// Initialize srv/EnrolStaff message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * acare_msgs__srv__EnrolStaff_Response
 * )) before or use
 * acare_msgs__srv__EnrolStaff_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Response__init(acare_msgs__srv__EnrolStaff_Response * msg);

/// Finalize srv/EnrolStaff message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Response__fini(acare_msgs__srv__EnrolStaff_Response * msg);

/// Create srv/EnrolStaff message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * acare_msgs__srv__EnrolStaff_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
acare_msgs__srv__EnrolStaff_Response *
acare_msgs__srv__EnrolStaff_Response__create(void);

/// Destroy srv/EnrolStaff message.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Response__destroy(acare_msgs__srv__EnrolStaff_Response * msg);

/// Check for srv/EnrolStaff message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Response__are_equal(const acare_msgs__srv__EnrolStaff_Response * lhs, const acare_msgs__srv__EnrolStaff_Response * rhs);

/// Copy a srv/EnrolStaff message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Response__copy(
  const acare_msgs__srv__EnrolStaff_Response * input,
  acare_msgs__srv__EnrolStaff_Response * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__srv__EnrolStaff_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__srv__EnrolStaff_Response__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__srv__EnrolStaff_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__srv__EnrolStaff_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/EnrolStaff messages.
/**
 * It allocates the memory for the number of elements and calls
 * acare_msgs__srv__EnrolStaff_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Response__Sequence__init(acare_msgs__srv__EnrolStaff_Response__Sequence * array, size_t size);

/// Finalize array of srv/EnrolStaff messages.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Response__Sequence__fini(acare_msgs__srv__EnrolStaff_Response__Sequence * array);

/// Create array of srv/EnrolStaff messages.
/**
 * It allocates the memory for the array and calls
 * acare_msgs__srv__EnrolStaff_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
acare_msgs__srv__EnrolStaff_Response__Sequence *
acare_msgs__srv__EnrolStaff_Response__Sequence__create(size_t size);

/// Destroy array of srv/EnrolStaff messages.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Response__Sequence__destroy(acare_msgs__srv__EnrolStaff_Response__Sequence * array);

/// Check for srv/EnrolStaff message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Response__Sequence__are_equal(const acare_msgs__srv__EnrolStaff_Response__Sequence * lhs, const acare_msgs__srv__EnrolStaff_Response__Sequence * rhs);

/// Copy an array of srv/EnrolStaff messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Response__Sequence__copy(
  const acare_msgs__srv__EnrolStaff_Response__Sequence * input,
  acare_msgs__srv__EnrolStaff_Response__Sequence * output);

/// Initialize srv/EnrolStaff message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * acare_msgs__srv__EnrolStaff_Event
 * )) before or use
 * acare_msgs__srv__EnrolStaff_Event__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Event__init(acare_msgs__srv__EnrolStaff_Event * msg);

/// Finalize srv/EnrolStaff message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Event__fini(acare_msgs__srv__EnrolStaff_Event * msg);

/// Create srv/EnrolStaff message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * acare_msgs__srv__EnrolStaff_Event__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
acare_msgs__srv__EnrolStaff_Event *
acare_msgs__srv__EnrolStaff_Event__create(void);

/// Destroy srv/EnrolStaff message.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Event__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Event__destroy(acare_msgs__srv__EnrolStaff_Event * msg);

/// Check for srv/EnrolStaff message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Event__are_equal(const acare_msgs__srv__EnrolStaff_Event * lhs, const acare_msgs__srv__EnrolStaff_Event * rhs);

/// Copy a srv/EnrolStaff message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Event__copy(
  const acare_msgs__srv__EnrolStaff_Event * input,
  acare_msgs__srv__EnrolStaff_Event * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_type_hash_t *
acare_msgs__srv__EnrolStaff_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeDescription *
acare_msgs__srv__EnrolStaff_Event__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource *
acare_msgs__srv__EnrolStaff_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
const rosidl_runtime_c__type_description__TypeSource__Sequence *
acare_msgs__srv__EnrolStaff_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/EnrolStaff messages.
/**
 * It allocates the memory for the number of elements and calls
 * acare_msgs__srv__EnrolStaff_Event__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Event__Sequence__init(acare_msgs__srv__EnrolStaff_Event__Sequence * array, size_t size);

/// Finalize array of srv/EnrolStaff messages.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Event__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Event__Sequence__fini(acare_msgs__srv__EnrolStaff_Event__Sequence * array);

/// Create array of srv/EnrolStaff messages.
/**
 * It allocates the memory for the array and calls
 * acare_msgs__srv__EnrolStaff_Event__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
acare_msgs__srv__EnrolStaff_Event__Sequence *
acare_msgs__srv__EnrolStaff_Event__Sequence__create(size_t size);

/// Destroy array of srv/EnrolStaff messages.
/**
 * It calls
 * acare_msgs__srv__EnrolStaff_Event__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
void
acare_msgs__srv__EnrolStaff_Event__Sequence__destroy(acare_msgs__srv__EnrolStaff_Event__Sequence * array);

/// Check for srv/EnrolStaff message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Event__Sequence__are_equal(const acare_msgs__srv__EnrolStaff_Event__Sequence * lhs, const acare_msgs__srv__EnrolStaff_Event__Sequence * rhs);

/// Copy an array of srv/EnrolStaff messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_acare_msgs
bool
acare_msgs__srv__EnrolStaff_Event__Sequence__copy(
  const acare_msgs__srv__EnrolStaff_Event__Sequence * input,
  acare_msgs__srv__EnrolStaff_Event__Sequence * output);
#ifdef __cplusplus
}
#endif

#endif  // ACARE_MSGS__SRV__DETAIL__ENROL_STAFF__FUNCTIONS_H_

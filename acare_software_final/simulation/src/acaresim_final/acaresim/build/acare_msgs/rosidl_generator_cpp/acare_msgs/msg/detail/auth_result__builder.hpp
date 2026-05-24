// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from acare_msgs:msg/AuthResult.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "acare_msgs/msg/auth_result.hpp"


#ifndef ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__BUILDER_HPP_
#define ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "acare_msgs/msg/detail/auth_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace acare_msgs
{

namespace msg
{

namespace builder
{

class Init_AuthResult_voice_confidence
{
public:
  explicit Init_AuthResult_voice_confidence(::acare_msgs::msg::AuthResult & msg)
  : msg_(msg)
  {}
  ::acare_msgs::msg::AuthResult voice_confidence(::acare_msgs::msg::AuthResult::_voice_confidence_type arg)
  {
    msg_.voice_confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

class Init_AuthResult_face_confidence
{
public:
  explicit Init_AuthResult_face_confidence(::acare_msgs::msg::AuthResult & msg)
  : msg_(msg)
  {}
  Init_AuthResult_voice_confidence face_confidence(::acare_msgs::msg::AuthResult::_face_confidence_type arg)
  {
    msg_.face_confidence = std::move(arg);
    return Init_AuthResult_voice_confidence(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

class Init_AuthResult_face_verified
{
public:
  explicit Init_AuthResult_face_verified(::acare_msgs::msg::AuthResult & msg)
  : msg_(msg)
  {}
  Init_AuthResult_face_confidence face_verified(::acare_msgs::msg::AuthResult::_face_verified_type arg)
  {
    msg_.face_verified = std::move(arg);
    return Init_AuthResult_face_confidence(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

class Init_AuthResult_success
{
public:
  explicit Init_AuthResult_success(::acare_msgs::msg::AuthResult & msg)
  : msg_(msg)
  {}
  Init_AuthResult_face_verified success(::acare_msgs::msg::AuthResult::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_AuthResult_face_verified(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

class Init_AuthResult_role
{
public:
  explicit Init_AuthResult_role(::acare_msgs::msg::AuthResult & msg)
  : msg_(msg)
  {}
  Init_AuthResult_success role(::acare_msgs::msg::AuthResult::_role_type arg)
  {
    msg_.role = std::move(arg);
    return Init_AuthResult_success(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

class Init_AuthResult_name
{
public:
  explicit Init_AuthResult_name(::acare_msgs::msg::AuthResult & msg)
  : msg_(msg)
  {}
  Init_AuthResult_role name(::acare_msgs::msg::AuthResult::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_AuthResult_role(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

class Init_AuthResult_user_id
{
public:
  Init_AuthResult_user_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AuthResult_name user_id(::acare_msgs::msg::AuthResult::_user_id_type arg)
  {
    msg_.user_id = std::move(arg);
    return Init_AuthResult_name(msg_);
  }

private:
  ::acare_msgs::msg::AuthResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::acare_msgs::msg::AuthResult>()
{
  return acare_msgs::msg::builder::Init_AuthResult_user_id();
}

}  // namespace acare_msgs

#endif  // ACARE_MSGS__MSG__DETAIL__AUTH_RESULT__BUILDER_HPP_

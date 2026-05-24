#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__RobotState() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__RobotState__init(msg: *mut RobotState) -> bool;
    fn acare_msgs__msg__RobotState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotState>, size: usize) -> bool;
    fn acare_msgs__msg__RobotState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotState>);
    fn acare_msgs__msg__RobotState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotState>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotState>) -> bool;
}

// Corresponds to acare_msgs__msg__RobotState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub active_user_id: rosidl_runtime_rs::String,

}



impl Default for RobotState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__RobotState__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__RobotState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__RobotState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__RobotState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__RobotState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotState where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/RobotState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__RobotState() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__StateTransition() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__StateTransition__init(msg: *mut StateTransition) -> bool;
    fn acare_msgs__msg__StateTransition__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<StateTransition>, size: usize) -> bool;
    fn acare_msgs__msg__StateTransition__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<StateTransition>);
    fn acare_msgs__msg__StateTransition__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<StateTransition>, out_seq: *mut rosidl_runtime_rs::Sequence<StateTransition>) -> bool;
}

// Corresponds to acare_msgs__msg__StateTransition
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StateTransition {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for StateTransition {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__StateTransition__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__StateTransition__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for StateTransition {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__StateTransition__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__StateTransition__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__StateTransition__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for StateTransition {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for StateTransition where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/StateTransition";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__StateTransition() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__Intent() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__Intent__init(msg: *mut Intent) -> bool;
    fn acare_msgs__msg__Intent__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Intent>, size: usize) -> bool;
    fn acare_msgs__msg__Intent__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Intent>);
    fn acare_msgs__msg__Intent__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Intent>, out_seq: *mut rosidl_runtime_rs::Sequence<Intent>) -> bool;
}

// Corresponds to acare_msgs__msg__Intent
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Intent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub action: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub destination: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,

}



impl Default for Intent {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__Intent__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__Intent__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Intent {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__Intent__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__Intent__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__Intent__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Intent {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Intent where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/Intent";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__Intent() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__ValidatedIntent() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__ValidatedIntent__init(msg: *mut ValidatedIntent) -> bool;
    fn acare_msgs__msg__ValidatedIntent__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ValidatedIntent>, size: usize) -> bool;
    fn acare_msgs__msg__ValidatedIntent__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ValidatedIntent>);
    fn acare_msgs__msg__ValidatedIntent__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ValidatedIntent>, out_seq: *mut rosidl_runtime_rs::Sequence<ValidatedIntent>) -> bool;
}

// Corresponds to acare_msgs__msg__ValidatedIntent
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ValidatedIntent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub action: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub user_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub authenticated: bool,

}



impl Default for ValidatedIntent {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__ValidatedIntent__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__ValidatedIntent__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ValidatedIntent {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__ValidatedIntent__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__ValidatedIntent__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__ValidatedIntent__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ValidatedIntent {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ValidatedIntent where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/ValidatedIntent";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__ValidatedIntent() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__SafetyAlert() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__SafetyAlert__init(msg: *mut SafetyAlert) -> bool;
    fn acare_msgs__msg__SafetyAlert__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SafetyAlert>, size: usize) -> bool;
    fn acare_msgs__msg__SafetyAlert__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SafetyAlert>);
    fn acare_msgs__msg__SafetyAlert__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SafetyAlert>, out_seq: *mut rosidl_runtime_rs::Sequence<SafetyAlert>) -> bool;
}

// Corresponds to acare_msgs__msg__SafetyAlert
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SafetyAlert {

    // This member is not documented.
    #[allow(missing_docs)]
    pub severity: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub source: rosidl_runtime_rs::String,

}



impl Default for SafetyAlert {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__SafetyAlert__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__SafetyAlert__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SafetyAlert {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__SafetyAlert__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__SafetyAlert__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__SafetyAlert__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SafetyAlert {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SafetyAlert where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/SafetyAlert";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__SafetyAlert() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__HandStatus() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__HandStatus__init(msg: *mut HandStatus) -> bool;
    fn acare_msgs__msg__HandStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<HandStatus>, size: usize) -> bool;
    fn acare_msgs__msg__HandStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<HandStatus>);
    fn acare_msgs__msg__HandStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<HandStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<HandStatus>) -> bool;
}

// Corresponds to acare_msgs__msg__HandStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct HandStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub hand_detected: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub is_open: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub palm_up: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,

}



impl Default for HandStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__HandStatus__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__HandStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for HandStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__HandStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__HandStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__HandStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for HandStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for HandStatus where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/HandStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__HandStatus() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__AuthResult() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__AuthResult__init(msg: *mut AuthResult) -> bool;
    fn acare_msgs__msg__AuthResult__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AuthResult>, size: usize) -> bool;
    fn acare_msgs__msg__AuthResult__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AuthResult>);
    fn acare_msgs__msg__AuthResult__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AuthResult>, out_seq: *mut rosidl_runtime_rs::Sequence<AuthResult>) -> bool;
}

// Corresponds to acare_msgs__msg__AuthResult
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AuthResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub user_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub role: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub face_verified: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub face_confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub voice_confidence: f32,

}



impl Default for AuthResult {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__AuthResult__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__AuthResult__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AuthResult {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__AuthResult__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__AuthResult__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__AuthResult__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AuthResult {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AuthResult where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/AuthResult";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__AuthResult() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__VisionResult() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__VisionResult__init(msg: *mut VisionResult) -> bool;
    fn acare_msgs__msg__VisionResult__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<VisionResult>, size: usize) -> bool;
    fn acare_msgs__msg__VisionResult__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<VisionResult>);
    fn acare_msgs__msg__VisionResult__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<VisionResult>, out_seq: *mut rosidl_runtime_rs::Sequence<VisionResult>) -> bool;
}

// Corresponds to acare_msgs__msg__VisionResult
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct VisionResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub found: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub zone: rosidl_runtime_rs::String,

}



impl Default for VisionResult {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__VisionResult__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__VisionResult__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for VisionResult {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__VisionResult__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__VisionResult__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__VisionResult__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for VisionResult {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for VisionResult where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/VisionResult";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__VisionResult() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__VisionSearchRequest() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__VisionSearchRequest__init(msg: *mut VisionSearchRequest) -> bool;
    fn acare_msgs__msg__VisionSearchRequest__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<VisionSearchRequest>, size: usize) -> bool;
    fn acare_msgs__msg__VisionSearchRequest__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<VisionSearchRequest>);
    fn acare_msgs__msg__VisionSearchRequest__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<VisionSearchRequest>, out_seq: *mut rosidl_runtime_rs::Sequence<VisionSearchRequest>) -> bool;
}

// Corresponds to acare_msgs__msg__VisionSearchRequest
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct VisionSearchRequest {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: rosidl_runtime_rs::String,

}



impl Default for VisionSearchRequest {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__VisionSearchRequest__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__VisionSearchRequest__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for VisionSearchRequest {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__VisionSearchRequest__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__VisionSearchRequest__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__VisionSearchRequest__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for VisionSearchRequest {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for VisionSearchRequest where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/VisionSearchRequest";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__VisionSearchRequest() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__ArmCommand() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__ArmCommand__init(msg: *mut ArmCommand) -> bool;
    fn acare_msgs__msg__ArmCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ArmCommand>, size: usize) -> bool;
    fn acare_msgs__msg__ArmCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ArmCommand>);
    fn acare_msgs__msg__ArmCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ArmCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<ArmCommand>) -> bool;
}

// Corresponds to acare_msgs__msg__ArmCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ArmCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_angles: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity_scale: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub accel_limit: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub blocking: bool,

}



impl Default for ArmCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__ArmCommand__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__ArmCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ArmCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__ArmCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__ArmCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__ArmCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ArmCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ArmCommand where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/ArmCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__ArmCommand() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__GripperCommand() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__GripperCommand__init(msg: *mut GripperCommand) -> bool;
    fn acare_msgs__msg__GripperCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GripperCommand>, size: usize) -> bool;
    fn acare_msgs__msg__GripperCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GripperCommand>);
    fn acare_msgs__msg__GripperCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GripperCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<GripperCommand>) -> bool;
}

// Corresponds to acare_msgs__msg__GripperCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub force_target: f32,

}



impl Default for GripperCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__GripperCommand__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__GripperCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GripperCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__GripperCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__GripperCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__GripperCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GripperCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GripperCommand where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/GripperCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__GripperCommand() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__MotionFeedback() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__MotionFeedback__init(msg: *mut MotionFeedback) -> bool;
    fn acare_msgs__msg__MotionFeedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotionFeedback>, size: usize) -> bool;
    fn acare_msgs__msg__MotionFeedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotionFeedback>);
    fn acare_msgs__msg__MotionFeedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotionFeedback>, out_seq: *mut rosidl_runtime_rs::Sequence<MotionFeedback>) -> bool;
}

// Corresponds to acare_msgs__msg__MotionFeedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionFeedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_positions: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_velocities: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_currents: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub temperatures: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_force: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_roll: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_pitch: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_yaw: f32,

}



impl Default for MotionFeedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__MotionFeedback__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__MotionFeedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotionFeedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__MotionFeedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__MotionFeedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__MotionFeedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotionFeedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotionFeedback where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/MotionFeedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__MotionFeedback() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__LogEvent() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__LogEvent__init(msg: *mut LogEvent) -> bool;
    fn acare_msgs__msg__LogEvent__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LogEvent>, size: usize) -> bool;
    fn acare_msgs__msg__LogEvent__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LogEvent>);
    fn acare_msgs__msg__LogEvent__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LogEvent>, out_seq: *mut rosidl_runtime_rs::Sequence<LogEvent>) -> bool;
}

// Corresponds to acare_msgs__msg__LogEvent
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LogEvent {

    // This member is not documented.
    #[allow(missing_docs)]
    pub event_type: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub user_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tool: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub description: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub voice_e2e_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vision_search_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub total_task_ms: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub safety_severity: rosidl_runtime_rs::String,

}



impl Default for LogEvent {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__LogEvent__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__LogEvent__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LogEvent {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__LogEvent__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__LogEvent__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__LogEvent__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LogEvent {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LogEvent where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/LogEvent";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__LogEvent() }
  }
}


#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__EmergencySignal() -> *const std::ffi::c_void;
}

#[link(name = "acare_msgs__rosidl_generator_c")]
extern "C" {
    fn acare_msgs__msg__EmergencySignal__init(msg: *mut EmergencySignal) -> bool;
    fn acare_msgs__msg__EmergencySignal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EmergencySignal>, size: usize) -> bool;
    fn acare_msgs__msg__EmergencySignal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EmergencySignal>);
    fn acare_msgs__msg__EmergencySignal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EmergencySignal>, out_seq: *mut rosidl_runtime_rs::Sequence<EmergencySignal>) -> bool;
}

// Corresponds to acare_msgs__msg__EmergencySignal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EmergencySignal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub source: rosidl_runtime_rs::String,

}



impl Default for EmergencySignal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !acare_msgs__msg__EmergencySignal__init(&mut msg as *mut _) {
        panic!("Call to acare_msgs__msg__EmergencySignal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EmergencySignal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__EmergencySignal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__EmergencySignal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { acare_msgs__msg__EmergencySignal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EmergencySignal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EmergencySignal where Self: Sized {
  const TYPE_NAME: &'static str = "acare_msgs/msg/EmergencySignal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__acare_msgs__msg__EmergencySignal() }
  }
}



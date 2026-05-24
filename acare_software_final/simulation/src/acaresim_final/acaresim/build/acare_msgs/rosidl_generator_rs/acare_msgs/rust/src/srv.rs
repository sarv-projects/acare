#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to acare_msgs__srv__EnrolStaff_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EnrolStaff_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub role: std::string::String,

}



impl Default for EnrolStaff_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EnrolStaff_Request::default())
  }
}

impl rosidl_runtime_rs::Message for EnrolStaff_Request {
  type RmwMsg = super::srv::rmw::EnrolStaff_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        role: msg.role.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        role: msg.role.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      role: msg.role.to_string(),
    }
  }
}


// Corresponds to acare_msgs__srv__EnrolStaff_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EnrolStaff_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub staff_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for EnrolStaff_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EnrolStaff_Response::default())
  }
}

impl rosidl_runtime_rs::Message for EnrolStaff_Response {
  type RmwMsg = super::srv::rmw::EnrolStaff_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        staff_id: msg.staff_id.as_str().into(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        staff_id: msg.staff_id.as_str().into(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      staff_id: msg.staff_id.to_string(),
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "acare_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__acare_msgs__srv__EnrolStaff() -> *const std::ffi::c_void;
}

// Corresponds to acare_msgs__srv__EnrolStaff
#[allow(missing_docs, non_camel_case_types)]
pub struct EnrolStaff;

impl rosidl_runtime_rs::Service for EnrolStaff {
    type Request = EnrolStaff_Request;
    type Response = EnrolStaff_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__acare_msgs__srv__EnrolStaff() }
    }
}



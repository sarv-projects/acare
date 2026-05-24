# generated from rosidl_generator_py/resource/_idl.py.em
# with input from acare_msgs:msg/AuthResult.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_AuthResult(type):
    """Metaclass of message 'AuthResult'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('acare_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'acare_msgs.msg.AuthResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__auth_result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__auth_result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__auth_result
            cls._TYPE_SUPPORT = module.type_support_msg__msg__auth_result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__auth_result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class AuthResult(metaclass=Metaclass_AuthResult):
    """Message class 'AuthResult'."""

    __slots__ = [
        '_user_id',
        '_name',
        '_role',
        '_success',
        '_face_verified',
        '_face_confidence',
        '_voice_confidence',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'user_id': 'string',
        'name': 'string',
        'role': 'string',
        'success': 'boolean',
        'face_verified': 'boolean',
        'face_confidence': 'float',
        'voice_confidence': 'float',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.user_id = kwargs.get('user_id', str())
        self.name = kwargs.get('name', str())
        self.role = kwargs.get('role', str())
        self.success = kwargs.get('success', bool())
        self.face_verified = kwargs.get('face_verified', bool())
        self.face_confidence = kwargs.get('face_confidence', float())
        self.voice_confidence = kwargs.get('voice_confidence', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.user_id != other.user_id:
            return False
        if self.name != other.name:
            return False
        if self.role != other.role:
            return False
        if self.success != other.success:
            return False
        if self.face_verified != other.face_verified:
            return False
        if self.face_confidence != other.face_confidence:
            return False
        if self.voice_confidence != other.voice_confidence:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def user_id(self):
        """Message field 'user_id'."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'user_id' field must be of type 'str'"
        self._user_id = value

    @builtins.property
    def name(self):
        """Message field 'name'."""
        return self._name

    @name.setter
    def name(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'name' field must be of type 'str'"
        self._name = value

    @builtins.property
    def role(self):
        """Message field 'role'."""
        return self._role

    @role.setter
    def role(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'role' field must be of type 'str'"
        self._role = value

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def face_verified(self):
        """Message field 'face_verified'."""
        return self._face_verified

    @face_verified.setter
    def face_verified(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'face_verified' field must be of type 'bool'"
        self._face_verified = value

    @builtins.property
    def face_confidence(self):
        """Message field 'face_confidence'."""
        return self._face_confidence

    @face_confidence.setter
    def face_confidence(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'face_confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'face_confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._face_confidence = value

    @builtins.property
    def voice_confidence(self):
        """Message field 'voice_confidence'."""
        return self._voice_confidence

    @voice_confidence.setter
    def voice_confidence(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'voice_confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'voice_confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._voice_confidence = value

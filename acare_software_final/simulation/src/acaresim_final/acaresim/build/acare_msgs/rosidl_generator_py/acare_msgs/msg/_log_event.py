# generated from rosidl_generator_py/resource/_idl.py.em
# with input from acare_msgs:msg/LogEvent.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_LogEvent(type):
    """Metaclass of message 'LogEvent'."""

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
                'acare_msgs.msg.LogEvent')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__log_event
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__log_event
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__log_event
            cls._TYPE_SUPPORT = module.type_support_msg__msg__log_event
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__log_event

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class LogEvent(metaclass=Metaclass_LogEvent):
    """Message class 'LogEvent'."""

    __slots__ = [
        '_event_type',
        '_user_id',
        '_tool',
        '_state',
        '_description',
        '_timestamp',
        '_voice_e2e_ms',
        '_vision_search_ms',
        '_motion_ms',
        '_total_task_ms',
        '_safety_severity',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'event_type': 'string',
        'user_id': 'string',
        'tool': 'string',
        'state': 'string',
        'description': 'string',
        'timestamp': 'int64',
        'voice_e2e_ms': 'int64',
        'vision_search_ms': 'int64',
        'motion_ms': 'int64',
        'total_task_ms': 'int64',
        'safety_severity': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
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
        self.event_type = kwargs.get('event_type', str())
        self.user_id = kwargs.get('user_id', str())
        self.tool = kwargs.get('tool', str())
        self.state = kwargs.get('state', str())
        self.description = kwargs.get('description', str())
        self.timestamp = kwargs.get('timestamp', int())
        self.voice_e2e_ms = kwargs.get('voice_e2e_ms', int())
        self.vision_search_ms = kwargs.get('vision_search_ms', int())
        self.motion_ms = kwargs.get('motion_ms', int())
        self.total_task_ms = kwargs.get('total_task_ms', int())
        self.safety_severity = kwargs.get('safety_severity', str())

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
        if self.event_type != other.event_type:
            return False
        if self.user_id != other.user_id:
            return False
        if self.tool != other.tool:
            return False
        if self.state != other.state:
            return False
        if self.description != other.description:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.voice_e2e_ms != other.voice_e2e_ms:
            return False
        if self.vision_search_ms != other.vision_search_ms:
            return False
        if self.motion_ms != other.motion_ms:
            return False
        if self.total_task_ms != other.total_task_ms:
            return False
        if self.safety_severity != other.safety_severity:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def event_type(self):
        """Message field 'event_type'."""
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'event_type' field must be of type 'str'"
        self._event_type = value

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
    def tool(self):
        """Message field 'tool'."""
        return self._tool

    @tool.setter
    def tool(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'tool' field must be of type 'str'"
        self._tool = value

    @builtins.property
    def state(self):
        """Message field 'state'."""
        return self._state

    @state.setter
    def state(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'state' field must be of type 'str'"
        self._state = value

    @builtins.property
    def description(self):
        """Message field 'description'."""
        return self._description

    @description.setter
    def description(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'description' field must be of type 'str'"
        self._description = value

    @builtins.property
    def timestamp(self):
        """Message field 'timestamp'."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'timestamp' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'timestamp' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._timestamp = value

    @builtins.property
    def voice_e2e_ms(self):
        """Message field 'voice_e2e_ms'."""
        return self._voice_e2e_ms

    @voice_e2e_ms.setter
    def voice_e2e_ms(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'voice_e2e_ms' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'voice_e2e_ms' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._voice_e2e_ms = value

    @builtins.property
    def vision_search_ms(self):
        """Message field 'vision_search_ms'."""
        return self._vision_search_ms

    @vision_search_ms.setter
    def vision_search_ms(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'vision_search_ms' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'vision_search_ms' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._vision_search_ms = value

    @builtins.property
    def motion_ms(self):
        """Message field 'motion_ms'."""
        return self._motion_ms

    @motion_ms.setter
    def motion_ms(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'motion_ms' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'motion_ms' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._motion_ms = value

    @builtins.property
    def total_task_ms(self):
        """Message field 'total_task_ms'."""
        return self._total_task_ms

    @total_task_ms.setter
    def total_task_ms(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'total_task_ms' field must be of type 'int'"
            assert value >= -9223372036854775808 and value < 9223372036854775808, \
                "The 'total_task_ms' field must be an integer in [-9223372036854775808, 9223372036854775807]"
        self._total_task_ms = value

    @builtins.property
    def safety_severity(self):
        """Message field 'safety_severity'."""
        return self._safety_severity

    @safety_severity.setter
    def safety_severity(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'safety_severity' field must be of type 'str'"
        self._safety_severity = value

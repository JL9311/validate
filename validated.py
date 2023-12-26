import re


class DataValidated:
    def __init__(self, type, msg, min_value=None, max_value=None, match=None):
        self.type = type
        self.msg = msg
        self.min_value = min_value
        self.max_value = max_value
        self.match = match

    @staticmethod
    def validate(obj):
        for attr, value in obj.__dict__.items():
            if hasattr(obj, attr):
                if hasattr(obj.__class__, attr):
                    attr_value = getattr(obj.__class__, attr)
                    if isinstance(attr_value, DataValidated):
                        if attr_value.type == Regular:
                            attr_value.type.validate(value, attr_value.match, attr_value.msg)
                        elif attr_value.type == Range:
                            attr_value.type.validate(value, attr_value.min_value, attr_value.max_value, attr_value.msg)
                        elif attr_value.type == Length:
                            attr_value.type.validate(value, attr_value.min_value, attr_value.max_value, attr_value.msg)
                        elif attr_value.type == NotNull:
                            attr_value.type.validate(value, attr_value.msg)
                        else:
                            pass

    @staticmethod
    def validate_with_out_error(obj):
        # 有错误返回False,错误字段列表，错误信息列表 无错误返回True,空，空
        error_list = []
        error_msg_list = []
        for attr, value in obj.__dict__.items():
            if hasattr(obj, attr):
                if hasattr(obj.__class__, attr):
                    attr_value = getattr(obj.__class__, attr)
                    if isinstance(attr_value, DataValidated):
                        if attr_value.type == Regular:
                            try:
                                attr_value.type.validate(value, attr_value.match, attr_value.msg)
                            except ValueError as e:
                                error_list.append(attr)
                                error_msg_list.append(e.args[0])
                        elif attr_value.type == Range:
                            try:
                                attr_value.type.validate(value, attr_value.min_value, attr_value.max_value, attr_value.msg)
                            except ValueError as e:
                                error_list.append(attr)
                                error_msg_list.append(e.args[0])
                        elif attr_value.type == Length:
                            try:
                                attr_value.type.validate(value, attr_value.min_value, attr_value.max_value, attr_value.msg)
                            except ValueError as e:
                                error_list.append(attr)
                                error_msg_list.append(e.args[0])
                        elif attr_value.type == NotNull:
                            try:
                                attr_value.type.validate(value, attr_value.msg)
                            except ValueError as e:
                                error_list.append(attr)
                                error_msg_list.append(e.args[0])
                        else:
                            pass
        if len(error_list) > 0:
            return False, error_list, error_msg_list
        return True, None, None


class NotNull:
    @staticmethod
    def validate(value, msg):
        if value is None:
            raise ValueError(msg)

    @staticmethod
    def validate_with_out_error(value, msg):
        if value is None:
            return False
        return True


class Range:
    @staticmethod
    def validate(value, min_value, max_value, msg):
        # min_value[0] max_value[0]为数值，min_value[1] max_value[1]为是否包含
        # min_value[1]为True时，表示包含，False时表示不包含
        if min_value[1] and max_value[1]:
            if not min_value[0] <= value <= max_value[0]:
                raise ValueError(msg)
        elif min_value[1] and not max_value[1]:
            if not min_value[0] <= value < max_value[0]:
                raise ValueError(msg)
        elif not min_value[1] and max_value[1]:
            if not min_value[0] < value <= max_value[0]:
                raise ValueError(msg)
        else:
            if not min_value[0] < value < max_value[0]:
                raise ValueError(msg)

    @staticmethod
    def validate_with_out_error(value, min_value, max_value, msg):
        # min_value[0] max_value[0]为数值，min_value[1] max_value[1]为是否包含
        # min_value[1]为True时，表示包含，False时表示不包含
        if min_value[1] and max_value[1]:
            if not min_value[0] <= value <= max_value[0]:
                return False
        elif min_value[1] and not max_value[1]:
            if not min_value[0] <= value < max_value[0]:
                return False
        elif not min_value[1] and max_value[1]:
            if not min_value[0] < value <= max_value[0]:
                return False
        else:
            if not min_value[0] < value < max_value[0]:
                return False
        return True


class Length:
    @staticmethod
    def validate(value, min_value, max_value, msg):
        if min_value[1] and max_value[1]:
            if not min_value[0] <= len(value) <= max_value[0]:
                raise ValueError(msg)
        elif min_value[1] and not max_value[1]:
            if not min_value[0] <= len(value) < max_value[0]:
                raise ValueError(msg)
        elif not min_value[1] and max_value[1]:
            if not min_value[0] < len(value) <= max_value[0]:
                raise ValueError(msg)
        else:
            if not min_value[0] < len(value) < max_value[0]:
                raise ValueError(msg)

    @staticmethod
    def validate_with_out_error(value, min_value, max_value, msg):
        if min_value[1] and max_value[1]:
            if not min_value[0] <= len(value) <= max_value[0]:
                return False
        elif min_value[1] and not max_value[1]:
            if not min_value[0] <= len(value) < max_value[0]:
                return False
        elif not min_value[1] and max_value[1]:
            if not min_value[0] < len(value) <= max_value[0]:
                return False
        else:
            if not min_value[0] < len(value) < max_value[0]:
                return False
        return True


class Regular:
    @staticmethod
    def validate(value, match, msg):
        if not re.match(match, value):
            raise ValueError(msg)

    @staticmethod
    def validate_with_out_error(value, match, msg):
        if not re.match(match, value):
            return False
        return True


def validate(**kwargs):
    def decorator(cls):
        for attr, value in kwargs.items():
            setattr(cls, attr, value)
        return cls

    return decorator

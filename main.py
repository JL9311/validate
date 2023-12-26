# 这是一个示例 Python 脚本。
from validated import DataValidated, validate, Length, Range, Regular


@validate(
    name=DataValidated(Length, "姓名长度要求大于等于10小于100", min_value=(2, True), max_value=(5, False)),
    age=DataValidated(Range, "办理年龄要求大于等于10小于100", min_value=(10, True), max_value=(60, False)),
    phone=DataValidated(Regular, "手机号码格式错误", match='^1[3-9]\d{9}$')
)
class Person:

    def __init__(self, name, age, phone):
        self.name = name
        self.age = age
        self.phone = phone


if __name__ == '__main__':
    person1 = Person("张", 115, '188888888888')
    res, item, msg = DataValidated.validate_with_out_error(person1)
    print(res, item, msg, "\n")

    person2 = Person("张三", 115, '188888888888')
    res, item, msg = DataValidated.validate_with_out_error(person2)
    print(res, item, msg, "\n")

    person3 = Person("张三", 15, '18888888888')
    res, item, msg = DataValidated.validate_with_out_error(person3)
    print(res, item, msg, "\n")

    person4 = Person("张三", 15, '18888888888')
    DataValidated.validate(person4)
    DataValidated.validate(person1)

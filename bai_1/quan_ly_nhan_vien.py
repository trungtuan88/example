from datetime import datetime
import calendar


def log_error(fn):
    def funDeco(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            print(("Có lỗi sảy ra khi thực hiện hàm %s:" + str(e)) %
                  (fn.__qualname__))
    return funDeco


def log_time(fn):
    def funDeco(*args, **kwargs):
        try:
            fn(*args, **kwargs)
            if fn.__name__ == "__init__":
                print("Khởi tạo lúc: " + str(datetime.now()))
            elif fn.__name__ == "setEmployeeInfo":
                print("Thay đổi lúc: " + str(datetime.now()))
        except Exception as e:
            print(("Có lỗi sảy ra khi thực hiện hàm %s:" + str(e)) %
                  (fn.__qualname__))
    return funDeco


class Employees():
    @log_error
    @log_time
    def __init__(self, name, employeeID, year, add, phone, email, department, position):
        self.name = name
        self.employeeID = employeeID
        self.year = year
        self.add = add
        self.phone = phone
        self.email = email
        self.department = department
        self.position = position
        department.addEmployee(self)

    @log_error
    def getEmployeeInfo(self):
        print(("Tên nhân viên: %s | ID: %s | Năm sinh: %s | Địa chỉ: %s | Điện Thoại: %s | Email: %s | Bộ Phận: %s | Vị Trí: %s") % (
            self.name, self.employeeID, self.year, self.add, self.phone, self.email, self.department.name, self.position))
        return [self.name, self.year, self.add, self.phone, self.email, self.department, self.position]

    @log_error
    @log_time
    def setEmployeeInfo(self, info):
        old_department = self.department
        self.name = info.get('name', self.name)
        self.employeeID = info.get('employeeID', self.employeeID)
        self.year = info.get('year', self.year)
        self.add = info.get('add', self.add)
        self.phone = info.get('phone', self.phone)
        self.email = info.get('email', self.email)
        self.department = info.get('department', self.department)
        self.position = info.get('position', self.position)
        if old_department != self.department:
            self.department.addEmployee(self)
            old_department.removeEmployee(self)

    def _is_complete(self):
        return all([self.name, self.employeeID, self.year, self.add, self.phone, self.email,
                    self.department, self.position])

    @classmethod
    def create(cls, list_info):
        employee = cls(*list_info)
        if employee._is_complete():
            return employee
        else:
            return None


class FullTimeEmployee(Employees):
    base_salary = 8000000
    base_time = 22
    base_leave = 12

    @log_error
    def __init__(self, name, employeeID, year, add, phone, email, department, position, leave=12, overtime=0):
        super().__init__(name, employeeID, year, add, phone, email, department, position)
        self.leave = leave
        self.overtime = overtime
        self.calculateSalary()

    def calculateLeave(self):
        self.numLeave = self.base_leave - self.leave

    def calculateSalary(self):
        num_days = calendar.monthrange(
            datetime.now().year, datetime.now().month,)[1]
        list_days = calendar.monthcalendar(
            datetime.now().year, datetime.now().month)
        num_sundays = sum(1 for i in list_days if i[-1])
        num_saturdays = sum(1 for i in list_days if i[-2])
        # day_off = num_sundays + num_saturdays
        day_working = num_days - (num_sundays + num_saturdays) - self.leave

        self.salary = (self.base_salary * day_working)/self.base_time + self.leave * (
            (self.base_salary/self.base_time) * 0.75) + ((self.base_salary/self.base_time)/8 * self.overtime * 1.5)

        return self.salary

    @log_error
    def setEmployeeInfo(self, info):
        super(FullTimeEmployee, self).setEmployeeInfo(info)
        self.leave = info.get('leave', self.leave)
        self.overtime = info.get('overtime', self.overtime)

        self.calculateSalary()
        self.calculateLeave()


class PartTimeEmployee(Employees):
    base_time_salary = 30000

    @log_error
    def __init__(self, name, employeeID, year, add, phone, email, department, position, worktime=0):
        super().__init__(name, employeeID, year, add, phone, email, department, position)
        self.worktime = worktime

    @log_error
    def setEmployeeInfo(self, info):
        super(PartTimeEmployee, self).setEmployeeInfo(info)
        self.worktime = info.get('worktime', self.worktime)
        self.calculateSalary()

    def calculateSalary(self):
        self.salary = self.worktime * self.base_time_salary


class Manager(FullTimeEmployee):
    base_bonus = 500000
    base_salary = 8000000

    @log_error
    def __init__(self, name, employeeID, year, add, phone, email, department, position, leave=12, overtime=0):
        self.numEmployee = department.num
        super().__init__(name, employeeID, year, add, phone,
                         email, department, position, leave, overtime)

    def NumEmployee(self):
        self.numEmployee = self.department.num

    def calculateSalary(self):
        salary = super(Manager, self).calculateSalary()
        self.salary = salary + self.numEmployee * self.base_bonus

    @log_error
    def setEmployeeInfo(self, info):
        super(Manager, self).setEmployeeInfo(info)
        self.NumEmployee()


class Department():
    @log_error
    @log_time
    def __init__(self, name, manager=None):
        self.name = name
        self.num = 0
        self.manager = manager
        self.employees = []

    def addEmployee(self, employee):
        self.num += 1
        self.employees.append(employee)

    def removeEmployee(self, employee):
        self.num -= 1
        self.employees.remove(employee)

    def SetDepartmentInfo(self, info):
        try:
            self.name = info.get('name', self.name)
            self.manager = info.get('manager', self.manager)
        except:
            print("Dữ liệu đầu vào không đúng")

    def _is_complete(self):
        return bool(self.name)

    @classmethod
    def create(cls, list_info):
        department = cls(*list_info)
        if department._is_complete():
            return department
        else:
            return None

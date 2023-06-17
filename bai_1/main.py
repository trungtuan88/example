import os

from datetime import datetime
from quan_ly_nhan_vien import FullTimeEmployee, PartTimeEmployee, Manager, Department

employees = {}
departments = {}
employee_ids = 0
department_ids = 0
employee_ids = 0
department_ids = 0


class createEmployee():
    @staticmethod
    def create():
        global employees
        name = input("Nhập tên nhân viên : ")
        while not name:
            input("Tên nhân viên không được bỏ trống - Vui lòng ấn Enter để nhập lại")
            name = input("Nhập tên nhân viên : ")
        ID = input("Nhập mã nhân viên: ")
        while True:
            try:
                year = input("Nhập năm sinh : ")
                int_year = int(year)
                if int_year >= datetime.now().year:
                    raise
                break
            except:
                print("Năm sinh không đúng - Vui lòng nhập lại")

        add = input("Nhập địa chỉ nhân viên: ")
        phone = input("Nhập số điện thoại: ")
        email = input("Nhập địa chỉ email: ")

        position = input("vị trí làm việc: ")

        return [name, ID, year, add, phone, email, position]

    @staticmethod
    def create_deparment(info):
        if not departments:
            print("Chưa có phòng ban nào được thành lập. Yêu cầu tạo phòng ban mới:")
            check = False
            while not check:
                check = create_Department.create()

        print("Nhân viên thuộc phòng ban: ")
        for key, vaule in departments.items():
            print(("Nhấn %s để chọn nhân viên %s thuộc phòng ban %s") %
                  (key, info[0], vaule.name))

        while True:
            try:
                key_input = int(input("Nhân viên thuộc phòng: "))
                if key_input in departments.keys():
                    department = departments.get(key_input, None)
                    break
                else:
                    print("Bạn chọn không đúng tên phòng")
            except:
                print("Bạn phải nhập số")

        info.insert(-1, department)

        return info


class create_FullTimeEmployee(createEmployee):
    @staticmethod
    def create():
        info = super(create_FullTimeEmployee, create_FullTimeEmployee).create()
        info = create_FullTimeEmployee.create_deparment(info)
        employee = FullTimeEmployee.create(info)
        if not employee:
            print("Thông tin không đầy đủ - Vui lòng nhập lại thông tin")
            return False
        employees.update({employee_seq_ids(): employee})
        return True


class create_PartTimeEmployee(createEmployee):
    @staticmethod
    def create():
        info = super(create_PartTimeEmployee, create_PartTimeEmployee).create()
        info = create_PartTimeEmployee.create_deparment(info)
        employee = PartTimeEmployee.create(info)
        if not employee:
            print("Thông tin không đầy đủ - Vui lòng nhập lại thông tin")
            return False
        employees.update({employee_seq_ids(): employee})
        return True


class create_Manager(createEmployee):
    @staticmethod
    def create():
        global employees
        department = None
        info = super(create_Manager, create_Manager).create()
        if not departments:
            print("Chưa có phòng ban nào được thành lập.:")
            print("Nhấn Y để tạo phòng ban mới: ")
            print("Nhấn N để bỏ qua bước này: ")
            while True:
                key_selection = input("Nhập Y/N : ")
                if key_selection == "y":
                    create_Department.create()
                    break
                elif key_selection == "n":
                    break
                else:
                    print("Bạn nhập không đúng yêu cầu")

        for key, vaule in departments.items():
            check = True
            print(("Nhấn %s để chọn nhân viên: %s quản lý %s") %
                  (key, info[0], vaule.name))

        if check:
            print("Ấn Enter để bỏ qua")
            while True:
                try:
                    key_input = input(
                        "Chọn tên nhân viên quản lý phòng ( hoặc để trống ): ")
                    if not key_input:
                        department = None
                        break
                    elif int(key_input) in departments.keys():
                        department = departments.get(int(key_input), None)
                        break
                    else:
                        print("Bạn chọn không đúng")
                except:
                    print("Bạn phải nhập số hoặc để trống")

        info.insert(-1, department)
        employee = Manager.create(info)
        if not employee:
            print("Thông tin không đầy đủ - Vui lòng nhập lại thông tin")
            return False
        employees.update({employee_seq_ids(): employee})
        return True


class create_Department():
    @staticmethod
    def create():
        global departments
        employee = None
        check = False
        name = input("Nhập tên phòng ban : ")
        while not name:
            input("Tên phòng ban không được bỏ trống - Vui lòng ấn Enter để nhập lại")
            name = input("Nhập tên phòng ban : ")

        for key, vaule in employees.items():
            if vaule.__class__ == "Manager":
                check = True
                print(("Nhấn %s để chọn nhân viên %s quản lý phòng ban %s") %
                      (key, vaule.name, name))
        if check:
            while True:
                try:
                    key_input = input(
                        "Chọn tên nhân viên quản lý phòng ( hoặc để trống ): ")
                    if not key_input:
                        employee = None
                        break
                    elif int(key_input) in employees.keys():
                        employee = employees.get(key_input, None)
                        break
                    else:
                        print("Bạn chọn không đúng")
                except:
                    print("Bạn phải nhập số hoặc để trống")

        else:
            print("Không tìm thấy nhân viên cấp quản lý. Vui lòng cập nhập sau:")

        manager = employee

        department = Department.create([name, manager])
        if not department:
            print("Thông tin không đầy đủ - Vui lòng nhập lại thông tin")
            return False
        departments.update({department_seq_ids(): department})
        return True


def search_info(info):
    dict_info = {}
    for i in employees:
        if info in vars(employees[i]).values():
            infor_employee = dict(vars(employees[i]))
            infor_employee.update(
                {'department': infor_employee['department'].name})
            print(("Thông Tin Nhân Viên: %s") % (infor_employee['name']))
            print(infor_employee)
            print("------------------------------------------------------")
            dict_info.update({i: employees[i]})
    return dict_info


def delete_employee(info):
    dict_info = {}
    for i in employees:
        if info in vars(employees[i]).values():
            dict_info.update({i: employees[i]})

    if dict_info:
        for i in dict_info:
            print(("Án %s đẻ xóa nhân viên có thông tin sau: ") % (i), end="")
            print(dict_info[i].getEmployeeInfo())
        while True:
            try:
                key_input = input(
                    "Lựa chọn nhân viên có vị trí hoặc ấn Enter để bỏ qua: ")
                if not key_input:
                    break
                elif int(key_input) in dict_info.keys():
                    del employees[int(key_input)]
                    break
                else:
                    print("Bạn chọn không đúng")
            except:
                print("Bạn phải nhập số hoặc để trống")


def wirte_employee(info):
    dict_info = {}
    for i in employees:
        if info in vars(employees[i]).values():
            dict_info.update({i: employees[i]})
    if dict_info:
        for i in dict_info:
            print(("Án %s đẻ chọn nhân viên có thông tin sau: ") % (i), end="")
            print(dict_info[i].getEmployeeInfo())
        while True:
            try:
                key_input = input(
                    "Lựa chọn nhân viên có vị trí hoặc ấn Enter để bỏ qua: ")
                if not key_input:
                    break
                elif int(key_input) in dict_info.keys():
                    employee_info = dict(vars(dict_info[int(key_input)]))
                    res = list(employee_info.keys())
                    res.remove('salary')
                    dict_key_employee = dict(enumerate(res, 1))
                    for i in dict_key_employee:
                        if dict_key_employee[i] == 'department':
                            employee_info.update(
                                {'department': employee_info[dict_key_employee[i]].name})
                        print(("Ấn %s để lựa chọn sửa thông tin %s: %s") % (
                            i, dict_key_employee[i], employee_info[dict_key_employee[i]]))
                    while True:
                        try:
                            key_select = input(
                                "Lựa chọn mục thông tin thay đổi hoặc ấn Enter để bỏ qua: ")
                            if not key_select:
                                break
                            elif int(key_select) in dict_key_employee.keys():
                                employee = employees[int(key_input)]
                                change_info = input(
                                    "Nhập thông tin cần thay đổi: ")
                                change_info = {
                                    dict_key_employee[int(key_select)]: change_info}
                                employee.setEmployeeInfo(change_info)
                                break
                            else:
                                print("Bạn chọn không đúng")
                        except:
                            print("Bạn phải nhập số hoặc để trống")
                    break
                else:
                    print("Bạn chọn không đúng")
            except:
                print("Bạn phải nhập số hoặc để trống")


def employee_seq_ids():
    global employee_ids
    employee_ids += 1
    return employee_ids


def department_seq_ids():
    global department_ids
    department_ids += 1
    return department_ids


def input_1():
    print("1 : Ấn B => Thêm Phòng Ban")
    print("2 : Ấn C => Thêm nhân viên")
    print("3 : Ấn Q => Thêm Quản Lý Phòng")
    print("4 : Ấn D => Xóa nhân viên viên")
    print("5 : Ấn S => Tìm nhân viên viên")
    print("6 : Ấn W => Sửa thông tin")
    print("7 : Ấn X => Thoát chương trình")
    fn = input("Ấn nút chức năng để thực hiện: ")
    return fn


print("Demo Chương Trình Quản Lý Nhân Viên")


while True:
    os.system('clear')
    fn = input_1()
    if fn == "c":
        os.system('clear')
        check = False
        print("Ấn F để thêm nhân viên Fulltime: ")
        print("Ấn P để thêm nhân viên Parttime: ")
        while True:
            key_input = input("Ấn F/P để thực hiện chức năng: ")
            if key_input == 'f':
                check = create_FullTimeEmployee.create()
                if check:
                    break
            elif key_input == 'p':
                check = create_PartTimeEmployee.create()
                if check:
                    break
            else:
                os.system('clear')
                print("Bạn nhập không đúng. Vui lòng nhập lại")
    elif fn == "b":
        os.system('clear')
        check = False
        while not check:
            check = create_Department.create()
    elif fn == "q":
        os.system('clear')
        check = False
        while not check:
            check = create_Manager.create()
    elif fn == "d":
        os.system('clear')
        key_input = input("Nhập thông tin nhân viên: ")
        delete_employee(key_input)
    elif fn == "w":
        os.system('clear')
        key_input = input("Nhập thông tin nhân viên: ")
        wirte_employee(key_input)
    elif fn == "s":
        os.system('clear')
        while True:
            info = input("Nhập thông tin cần tìm kiếm : ")
            search_info(info)
            print("Nhấn Enter để tiếp tục tìm kiếm")
            print("Nhập \"B\" để quay lại : ")
            key = input("Nhập lênh để thực hiện : ")
            if key == "b":
                break
    elif fn == "x":
        break

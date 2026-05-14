def dao_nguoc_list(lst):
    return lst[::-1]

input_list = input("Nhap danh sach cac so, tach nhau boi dau phay: ")
nums = list(map(int, input_list.split(',')))
print("Danh sach sau khi dao nguoc la:", dao_nguoc_list(nums))
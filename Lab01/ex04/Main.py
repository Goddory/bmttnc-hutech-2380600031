from SinhVien import SinhVien

class QuanLySinhVien:
    def __init__(self):
        self.danh_sach_sv = []
    
    def them_sinh_vien(self):
  
        print("\n--- THÊM SINH VIÊN ---")
        try:
            ten = input("Nhập tên sinh viên: ").strip()
            if not ten:
                print("Tên không được để trống!")
                return
            
            gioi_tinh = input("Nhập giới tính (Nam/Nữ): ").strip()
            chuyen_nganh = input("Nhập chuyên ngành: ").strip()
            
            diem_tb = float(input("Nhập điểm trung bình (0-10): "))
            if not (0 <= diem_tb <= 10):
                print("Điểm phải từ 0 đến 10!")
                return
            
            sv = SinhVien(ten, gioi_tinh, chuyen_nganh, diem_tb)
            self.danh_sach_sv.append(sv)
            print(f"✓ Thêm sinh viên thành công! ID: {sv.id}")
        except ValueError:
            print("Dữ liệu không hợp lệ!")
    
    def cap_nhat_sinh_vien(self):
        
        print("\n--- CẬP NHẬT THÔNG TIN SINH VIÊN ---")
        try:
            sv_id = int(input("Nhập ID sinh viên: "))
            sv = self._tim_sv_theo_id(sv_id)
            
            if sv is None:
                print(f"Không tìm thấy sinh viên ID {sv_id}")
                return
            
            print(f"Thông tin hiện tại: {sv}")
            print("(Nhấn Enter để giữ nguyên)")
            
            ten = input("Tên mới: ").strip() or None
            gioi_tinh = input("Giới tính mới: ").strip() or None
            chuyen_nganh = input("Chuyên ngành mới: ").strip() or None
            
            diem_str = input("Điểm TB mới: ").strip()
            diem_tb = float(diem_str) if diem_str else None
            
            if diem_tb is not None and not (0 <= diem_tb <= 10):
                print("Điểm phải từ 0 đến 10!")
                return
            
            sv.cap_nhat(ten, gioi_tinh, chuyen_nganh, diem_tb)
            print("Cập nhật thành công!")
        except ValueError:
            print("Dữ liệu không hợp lệ!")
    
    def xoa_sinh_vien(self):
    
        print("\n--- XÓA SINH VIÊN ---")
        try:
            sv_id = int(input("Nhập ID sinh viên cần xóa: "))
            sv = self._tim_sv_theo_id(sv_id)
            
            if sv is None:
                print(f"Không tìm thấy sinh viên ID {sv_id}")
                return
            
            print(f"Xóa: {sv}")
            xac_nhan = input("Xác nhận xóa (y/n)? ").lower()
            if xac_nhan == 'y':
                self.danh_sach_sv.remove(sv)
                print("✓ Xóa thành công!")
            else:
                print("Đã hủy xóa.")
        except ValueError:
            print("ID phải là số!")
    
    def tim_kiem_theo_ten(self):
        
        print("\n--- TÌM KIẾM SINH VIÊN ---")
        ten = input("Nhập tên cần tìm: ").strip().lower()
        
        ket_qua = [sv for sv in self.danh_sach_sv if ten in sv.ten.lower()]
        
        if not ket_qua:
            print(f"Không tìm thấy sinh viên nào tên '{ten}'")
        else:
            print(f"\nTìm thấy {len(ket_qua)} kết quả:")
            for sv in ket_qua:
                print(f"  {sv}")
    
    def sap_xep_theo_diem(self):
        
        if not self.danh_sach_sv:
            print("Danh sách rỗng!")
            return
        
        danh_sach_sap_xep = sorted(self.danh_sach_sv, key=lambda sv: sv.diem_tb, reverse=True)
        print("\n--- DANH SÁCH SINH VIÊN (SẮP XếP THEO ĐIỂM TB - GIẢM DẦN) ---")
        for sv in danh_sach_sap_xep:
            print(f"  {sv}")
    
    def sap_xep_theo_chuyen_nganh(self):
       
        if not self.danh_sach_sv:
            print("Danh sách rỗng!")
            return
        
        danh_sach_sap_xep = sorted(self.danh_sach_sv, key=lambda sv: sv.chuyen_nganh)
        print("\n--- DANH SÁCH SINH VIÊN (SẮP XếP THEO CHUYÊN NGÀNH) ---")
        for sv in danh_sach_sap_xep:
            print(f"  {sv}")
    
    def hien_thi_danh_sach(self):
        
        if not self.danh_sach_sv:
            print("Danh sách rỗng!")
            return
        
        print("\n--- DANH SÁCH TẤT CẢ SINH VIÊN ---")
        print(f"Tổng số sinh viên: {len(self.danh_sach_sv)}")
        for sv in self.danh_sach_sv:
            print(f"  {sv}")
    
    def _tim_sv_theo_id(self, sv_id):
     
        for sv in self.danh_sach_sv:
            if sv.id == sv_id:
                return sv
        return None
    
    def hien_thi_menu(self):
      
        while True:
            print("\n" + "="*60)
            print("CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN")
            print("="*60)
            print("1. Thêm sinh viên")
            print("2. Cập nhật thông tin sinh viên")
            print("3. Xóa sinh viên")
            print("4. Tìm kiếm sinh viên theo tên")
            print("5. Sắp xếp theo điểm trung bình")
            print("6. Sắp xếp theo chuyên ngành")
            print("7. Hiển thị danh sách sinh viên")
            print("0. Thoát")
            print("="*60)
            
            lua_chon = input("Chọn chức năng (0-7): ").strip()
            
            if lua_chon == "1":
                self.them_sinh_vien()
            elif lua_chon == "2":
                self.cap_nhat_sinh_vien()
            elif lua_chon == "3":
                self.xoa_sinh_vien()
            elif lua_chon == "4":
                self.tim_kiem_theo_ten()
            elif lua_chon == "5":
                self.sap_xep_theo_diem()
            elif lua_chon == "6":
                self.sap_xep_theo_chuyen_nganh()
            elif lua_chon == "7":
                self.hien_thi_danh_sach()
            elif lua_chon == "0":
                print("\nTạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ! Vui lòng thử lại.")

if __name__ == "__main__":
    ql = QuanLySinhVien()
    ql.hien_thi_menu()

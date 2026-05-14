class SinhVien:
    
    _id_counter = 1
    
    def __init__(self, ten, gioi_tinh, chuyen_nganh, diem_tb):
        self.id = SinhVien._id_counter
        SinhVien._id_counter += 1
        self.ten = ten
        self.gioi_tinh = gioi_tinh
        self.chuyen_nganh = chuyen_nganh
        self.diem_tb = diem_tb
    
    def tinh_hoc_luc(self):
      
        if self.diem_tb >= 8:
            return "Giỏi"
        elif self.diem_tb >= 6.5:
            return "Khá"
        elif self.diem_tb >= 5:
            return "Trung bình"
        else:
            return "Yếu"
    
    def __str__(self):
        
        return (f"ID: {self.id} | Tên: {self.ten} | Giới tính: {self.gioi_tinh} | "
                f"Chuyên ngành: {self.chuyen_nganh} | Điểm TB: {self.diem_tb} | "
                f"Học lực: {self.tinh_hoc_luc()}")
    
    def cap_nhat(self, ten=None, gioi_tinh=None, chuyen_nganh=None, diem_tb=None):
       
        if ten is not None:
            self.ten = ten
        if gioi_tinh is not None:
            self.gioi_tinh = gioi_tinh
        if chuyen_nganh is not None:
            self.chuyen_nganh = chuyen_nganh
        if diem_tb is not None:
            self.diem_tb = diem_tb

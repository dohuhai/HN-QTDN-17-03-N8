---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)



# 1. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 1.1. Clone project.
```
git clone https://gitlab.com/anhlta/odoo-fitdnu.git
```
```
cd odoo-fitdnu
```
```
git checkout cntt15_03
```


## 1.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết
```
sudo apt update
```

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 1.3. khởi tạo môi trường ảo.

```
python3.10 -m venv ./venv
```
Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

# 2. Setup database
Chạy lệnh
```
sudo apt install docker-compose
```
Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
docker-compose up -d
```

# 3. Setup tham số chạy cho hệ thống

## 3.1. Khởi tạo odoo.conf

Tạo file **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5433
xmlrpc_port = 8069
```
Có thể kế thừa từ **odoo.conf.template**


# 4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất
 ---

# 5. Chức năng hệ thống nhóm phát triển

Hệ thống **Quản lý Chấm công và Tính lương** được xây dựng trên nền tảng **Odoo 15**, áp dụng cho **Công ty TNHH Thương mại và Dịch vụ Minh Hải**.

Hệ thống hỗ trợ doanh nghiệp quản lý nhân viên, ghi nhận dữ liệu chấm công hằng ngày, tổng hợp công cuối tháng, tự động tạo phiếu lương và gửi email phiếu lương cho nhân viên.

Luồng nghiệp vụ chính:

```text
HRM → Chấm công → Tính lương → Gửi email phiếu lương
```

---

## 5.1. Quản lý nhân sự

Phân hệ HRM dùng để quản lý thông tin nhân viên như mã định danh, họ tên, email, số điện thoại, phòng ban và chức vụ.

Dữ liệu nhân viên trong HRM được dùng lại ở phân hệ Chấm công và Tính lương, giúp tránh nhập lại dữ liệu thủ công.

<img width="1902" height="931" alt="Quản lý nhân viên" src="assets/web/01_nhan_vien.png" />

---

## 5.2. Cấu hình lương cơ bản

Phân hệ Tính lương cho phép cấu hình lương cơ bản và các khoản phụ cấp của từng nhân viên.

Dữ liệu này được hệ thống sử dụng khi tạo phiếu lương tháng.

<img width="1902" height="931" alt="Cấu hình lương cơ bản" src="assets/web/02_luong_co_ban.png" />

---

## 5.3. Quản lý chấm công

Phân hệ Chấm công dùng để ghi nhận dữ liệu công hằng ngày của nhân viên, gồm ngày chấm công, trạng thái công, số giờ làm việc, số giờ tăng ca và người xác nhận.

<img width="1902" height="931" alt="Dữ liệu chấm công" src="assets/web/03_cham_cong.png" />

---

## 5.4. Chốt công tháng

Cuối tháng, người dùng bấm nút **Chốt công tháng** trong phân hệ Chấm công.

Khi bấm nút này, hệ thống tự động tổng hợp dữ liệu chấm công, lấy thông tin lương cơ bản, phụ cấp, khen thưởng, kỷ luật và tạo hoặc cập nhật phiếu lương tháng.

<img width="1902" height="931" alt="Chốt công tháng" src="assets/web/04_chot_cong_thang.png" />

---

## 5.5. Phiếu lương tháng

Sau khi chốt công tháng, hệ thống tự động tạo phiếu lương cho nhân viên.

Phiếu lương gồm các thông tin: nhân viên, mã định danh, tháng, năm, số ngày công, lương cơ bản, phụ cấp, khen thưởng, kỷ luật, bảo hiểm và thực lĩnh.

<img width="1902" height="931" alt="Phiếu lương tháng" src="assets/web/05_phieu_luong.png" />

---

## 5.6. Gửi email phiếu lương

Sau khi phiếu lương được xác nhận hoặc thanh toán, người dùng bấm nút **Gửi email phiếu lương**.

Hệ thống lấy email nhân viên từ HRM, gửi thông tin phiếu lương cho nhân viên và ghi nhận trạng thái **Đã gửi email** cùng **Ngày gửi email**.

<img width="1902" height="931" alt="Gửi email phiếu lương" src="assets/web/06_gui_email_phieu_luong.png" />

---

## 5.7. Kết quả đạt được

Hệ thống đã hoàn thiện các chức năng chính:

* Quản lý nhân viên trong HRM.
* Quản lý dữ liệu chấm công.
* Quản lý lương cơ bản, phụ cấp, khen thưởng và kỷ luật.
* Tự động chốt công tháng.
* Tự động tạo hoặc cập nhật phiếu lương.
* Xác nhận và thanh toán phiếu lương.
* Gửi email phiếu lương cho nhân viên.
* Áp dụng cho doanh nghiệp cụ thể: **Công ty TNHH Thương mại và Dịch vụ Minh Hải**.

Hệ thống đáp ứng đủ 03 mức yêu cầu:

* **Mức 1:** Có HRM, Chấm công, Tính lương và liên kết dữ liệu nhân viên.
* **Mức 2:** Có nút **Chốt công tháng** tự động tạo phiếu lương.
* **Mức 3:** Có chức năng **Gửi email phiếu lương** cho nhân viên.
   

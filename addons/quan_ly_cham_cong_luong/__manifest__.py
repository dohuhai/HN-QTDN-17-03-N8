{
    'name': 'Quản lý nhân sự',
    'version': '1.0',
    'summary': 'Tự động hóa chấm công, tính lương, thưởng phạt và bảo hiểm',
    'description': """
Module Quản lý nhân sự.

Gồm 2 phân hệ riêng:
- Chấm công: quản lý dữ liệu chấm công nhân viên.
- Tính lương: cấu hình lương, khen thưởng, kỷ luật và tạo phiếu lương tháng.

Dữ liệu chấm công là đầu vào phục vụ quá trình tính lương.
    """,
    'category': 'Human Resources',
    'author': 'Do Huu Hai',
    'depends': ['base','mail', 'ql_nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_luong_co_ban_views.xml',
        'views/hr_cham_cong_views.xml',
        'views/hr_khen_thuong_ky_luat_views.xml',
        'views/hr_phieu_luong_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}

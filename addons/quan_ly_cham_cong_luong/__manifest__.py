{
    'name': 'Quản lý Chấm công & Tính lương',
    'version': '1.0',
    'summary': 'Tự động hóa chấm công, tính lương, thưởng phạt và bảo hiểm',
    'description': '''
Module Quản lý Chấm công & Tính lương.
Kết nối dữ liệu nhân sự từ module ql_nhan_su.
Hỗ trợ cấu hình lương cơ bản, chấm công, khen thưởng, kỷ luật và tự động tính phiếu lương tháng.
    ''',
    'category': 'Human Resources',
    'author': 'Do Huu Hai',
    'depends': ['base', 'ql_nhan_su'],
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

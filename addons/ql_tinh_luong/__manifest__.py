{
    'name': 'Quản lý Chấm công & Tính lương',
    'version': '1.0',
    'summary': 'HRM Module - Chấm công và tính lương',
    'description': 'Module quản lý nhân viên, chấm công, tính lương và dashboard',
    'author': 'Your Team',
    'depends': ['base', 'nhan_su'],
    'data': [
	'security/ir.model.access.csv',
        'views/hr_phieu_luong_views.xml',
        'views/hr_dashboard_views.xml',
        'views/hr_dashboard_menu.xml',
    ],
    'installable': True,
    'application': True,
}

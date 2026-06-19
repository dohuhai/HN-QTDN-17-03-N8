from odoo import models, fields


class HRKhenThuongKyLuat(models.Model):
    _name = 'hr_khen_thuong_ky_luat'
    _description = 'Khen thưởng và kỷ luật nhân viên'
    _order = 'ngay_ap_dung desc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True
    )

    ma_dinh_danh = fields.Char(
        string='Mã định danh',
        related='nhan_vien_id.ma_dinh_danh',
        store=True
    )

    loai_quyet_dinh = fields.Selection([
        ('khen_thuong', 'Khen thưởng'),
        ('ky_luat', 'Kỷ luật phạt')
    ], string='Loại quyết định', required=True)

    so_tien = fields.Float(
        string='Số tiền',
        required=True,
        default=0.0
    )

    ngay_ap_dung = fields.Date(
        string='Ngày áp dụng',
        required=True,
        default=fields.Date.context_today
    )

    ly_do = fields.Text(
        string='Lý do'
    )

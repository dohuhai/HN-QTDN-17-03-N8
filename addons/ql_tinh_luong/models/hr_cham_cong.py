from odoo import models, fields


class HRChamCong(models.Model):
    _name = 'hr.cham.cong'
    _description = 'Chấm công nhân viên'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True
    )

    ngay = fields.Date(
        string='Ngày chấm công',
        required=True
    )

    thang = fields.Integer(
        string='Tháng',
        required=True
    )

    nam = fields.Integer(
        string='Năm',
        required=True
    )

    trang_thai = fields.Selection(
        [
            ('di_lam', 'Đi làm'),
            ('nghi', 'Nghỉ')
        ],
        string='Trạng thái',
        default='di_lam',
        required=True
    )

    ghi_chu = fields.Text(
        string='Ghi chú'
    )

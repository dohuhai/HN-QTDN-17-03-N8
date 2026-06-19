from odoo import models, fields, api


class HRChamCong(models.Model):
    _name = 'hr_cham_cong'
    _description = 'Bảng dữ liệu chấm công hằng ngày'
    _order = 'ngay_cham_cong desc'

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

    ngay_cham_cong = fields.Date(
        string='Ngày chấm công',
        required=True,
        default=fields.Date.context_today
    )

    trang_thai = fields.Selection([
        ('di_lam', 'Đi làm đủ ngày'),
        ('nua_ngay', 'Làm nửa ngày'),
        ('nghi_co_phep', 'Nghỉ có phép'),
        ('nghi_khong_phep', 'Nghỉ không phép')
    ], string='Trạng thái công', default='di_lam', required=True)

    so_gio_lam_viec = fields.Float(
        string='Số giờ làm việc',
        compute='_compute_so_gio_lam_viec',
        store=True
    )

    so_gio_tang_ca = fields.Float(
        string='Số giờ tăng ca',
        default=0.0
    )

    nguoi_xac_nhan = fields.Char(
        string='Người xác nhận'
    )

    ghi_chu = fields.Text(
        string='Ghi chú'
    )

    @api.depends('trang_thai')
    def _compute_so_gio_lam_viec(self):
        for record in self:
            if record.trang_thai == 'di_lam':
                record.so_gio_lam_viec = 8
            elif record.trang_thai == 'nua_ngay':
                record.so_gio_lam_viec = 4
            else:
                record.so_gio_lam_viec = 0

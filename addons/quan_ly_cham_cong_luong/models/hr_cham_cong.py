from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
import calendar


class HrChamCong(models.Model):
    _name = 'hr_cham_cong'
    _description = 'Quản lý chấm công'
    _order = 'ngay_cham_cong desc, id desc'

    ngay_cham_cong = fields.Date(
        string='Ngày chấm công',
        required=True,
        default=fields.Date.context_today
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True
    )

    ma_dinh_danh = fields.Char(
        string='Mã định danh',
        related='nhan_vien_id.ma_dinh_danh',
        store=True,
        readonly=True
    )

    trang_thai = fields.Selection([
        ('di_lam_du_ngay', 'Đi làm đủ ngày'),
        ('lam_nua_ngay', 'Làm nửa ngày'),
        ('nghi_co_phep', 'Nghỉ có phép'),
        ('nghi_khong_phep', 'Nghỉ không phép'),
        ('di_muon', 'Đi muộn'),
    ], string='Trạng thái công', required=True, default='di_lam_du_ngay')

    so_gio_lam_viec = fields.Float(
        string='Số giờ làm việc',
        compute='_compute_so_gio_lam_viec',
        store=True
    )

    so_gio_tang_ca = fields.Float(
        string='Số giờ tăng ca',
        default=0
    )

    nguoi_xac_nhan = fields.Many2one(
        'res.users',
        string='Người xác nhận',
        default=lambda self: self.env.user
    )

    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('trang_thai')
    def _compute_so_gio_lam_viec(self):
        for rec in self:
            if rec.trang_thai == 'di_lam_du_ngay':
                rec.so_gio_lam_viec = 8
            elif rec.trang_thai == 'lam_nua_ngay':
                rec.so_gio_lam_viec = 4
            elif rec.trang_thai == 'di_muon':
                rec.so_gio_lam_viec = 7
            else:
                rec.so_gio_lam_viec = 0

    def action_chot_cong_thang(self):
        for rec in self:
            if not rec.nhan_vien_id:
                raise UserError('Bạn cần chọn nhân viên trước khi chốt công.')

            if not rec.ngay_cham_cong:
                raise UserError('Bạn cần nhập ngày chấm công trước khi chốt công.')

            thang = rec.ngay_cham_cong.month
            nam = rec.ngay_cham_cong.year

            ngay_dau_thang = date(nam, thang, 1)
            ngay_cuoi_thang = date(nam, thang, calendar.monthrange(nam, thang)[1])

            cham_cong_records = self.search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', ngay_dau_thang),
                ('ngay_cham_cong', '<=', ngay_cuoi_thang),
            ])

            tong_gio_lam = sum(cham_cong_records.mapped('so_gio_lam_viec'))
            so_ngay_cong = tong_gio_lam / 8.0

            luong_cb = self.env['hr_luong_co_ban'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id)
            ], limit=1, order='id desc')

            luong_co_ban = luong_cb.luong_co_ban if luong_cb else 0

            phu_cap = 0
            if luong_cb:
                phu_cap = (
                    luong_cb.phu_cap_an_trua
                    + luong_cb.phu_cap_trach_nhiem
                    + luong_cb.phu_cap_khac
                )

            ktkl_records = self.env['hr_khen_thuong_ky_luat'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('ngay_ap_dung', '>=', ngay_dau_thang),
                ('ngay_ap_dung', '<=', ngay_cuoi_thang),
            ])

            tong_khen_thuong = 0
            tong_ky_luat = 0

            for dong in ktkl_records:
                if dong.loai_quyet_dinh in ['khen_thuong', 'thuong']:
                    tong_khen_thuong += dong.so_tien
                else:
                    tong_ky_luat += dong.so_tien

            tien_bao_hiem = luong_co_ban * 0.105

            phieu_luong = self.env['hr_phieu_luong'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('thang', '=', str(thang)),
                ('nam', '=', nam),
            ], limit=1)

            vals = {
                'ten_phieu_luong': 'Phiếu lương tháng %s/%s - %s' % (
                    thang,
                    nam,
                    rec.nhan_vien_id.display_name
                ),
                'nhan_vien_id': rec.nhan_vien_id.id,
                'thang': str(thang),
                'nam': nam,
                'so_ngay_cong_tinh_luong': so_ngay_cong,
                'luong_co_ban': luong_co_ban,
                'phu_cap': phu_cap,
                'tong_khen_thuong': tong_khen_thuong,
                'tong_ky_luat': tong_ky_luat,
                'tien_bao_hiem': tien_bao_hiem,
            }

            if phieu_luong:
                phieu_luong.write(vals)
            else:
                phieu_luong = self.env['hr_phieu_luong'].create(vals)

            return {
                'type': 'ir.actions.act_window',
                'name': 'Phiếu lương tháng',
                'res_model': 'hr_phieu_luong',
                'view_mode': 'form',
                'res_id': phieu_luong.id,
                'target': 'current',
            }

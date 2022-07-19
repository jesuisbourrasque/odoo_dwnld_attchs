from odoo import fields, models, api


class DepartmentPlan(models.Model):
    _name = "department.plan"
    _inherit = "mail.thread"
    _description = "Department Plan info"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    department_id = fields.Many2one("hr.department", string="Department")
    employee_id = fields.Many2one("hr.employee", string="Employee")

    employee_plans_ids = fields.One2many("employee.plan", "department_plan_id", string="Employee Plans")

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")
    planned_amount = fields.Monetary(string="Planned amount", compute="_get_metrics")

    planned_hours = fields.Integer(string="Planned hours", compute="_get_metrics")
    average_hourly_rate = fields.Float(string="Average hourly rate", compute="_get_metrics")

    @api.depends("planned_amount", "planned_hours", "average_hourly_rate")
    def _get_metrics(self):
        for record in self:
            record.planned_amount = sum(record.employee_plans_ids.mapped("planned_amount"))
            record.planned_hours = sum(record.employee_plans_ids.mapped("work_hours"))
            hourly_rates = record.employee_plans_ids.mapped("hourly_rate")
            try:
                record.average_hourly_rate = sum(hourly_rates)/len(hourly_rates)
            except ZeroDivisionError:
                record.average_hourly_rate = 0

    def download_attachments(self):

        return {"type": "ir.actions.act_url",
                "url": "/download_attachments?res_id={}".format(self.id),}
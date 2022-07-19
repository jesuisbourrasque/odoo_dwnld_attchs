from odoo import fields, models, api


class EmployeePlan(models.Model):
    _name = "employee.plan"
    _description = "Employee Plan info"

    employee_id = fields.Many2one("hr.employee", string="Employee")
    hourly_rate = fields.Float(string="Hourly rate")
    work_hours = fields.Integer(string="Work hours")

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")
    planned_amount = fields.Monetary(string="Planned amount", compute="_compute_planned_amount")

    department_plan_id = fields.Many2one("department.plan", readonly=True)

    @api.depends("planned_amount")
    def _compute_planned_amount(self):
        for record in self:
            record.planned_amount = record.hourly_rate * record.work_hours

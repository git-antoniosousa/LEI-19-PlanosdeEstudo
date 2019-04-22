from odoo import fields, models

class UC (models.Model):
    _name='planum.uc'
    _description='Unidade Curricular'
    _order='designacao asc'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código UC')
    designacao = fields.Char('Designação')
    ects=fields.Integer('Créditos ECTS')
    obrigatoria=fields.Boolean('Obrigatória?')
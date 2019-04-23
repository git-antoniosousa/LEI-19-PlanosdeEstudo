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
    ucs_plano_curso = fields.One2many('planum.uc_plano_curso', 'uc_id', 'UCs de Planos de Curso')
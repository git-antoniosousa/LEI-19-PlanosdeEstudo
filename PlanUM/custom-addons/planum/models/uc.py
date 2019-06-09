from odoo import fields, models, api
from odoo.exceptions import ValidationError

class UC (models.Model):
    _name='planum.uc'
    _description='Unidade Curricular'
    _order='designacao asc'
    _rec_name = 'codigo_designacao'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código UC')
    designacao = fields.Char('Designação')
    ects = fields.Integer('Créditos ECTS', default=5)
    obrigatoria = fields.Boolean('Obrigatória?')
    ucs_plano_curso = fields.One2many('planum.uc_plano_curso', 'uc_id', 'UCs de Planos de Curso')
    codigo_designacao = fields.Char(compute='_compute_codigo_designacao')

    @api.depends('codigo', 'designacao')
    def _compute_codigo_designacao(self):
        for uc in self:
            uc.codigo_designacao = uc.codigo + ' - ' + uc.designacao

    @api.constrains('codigo', 'designacao', 'ects')
    def uc_check(self):
        if not self.codigo or not self.designacao or not self.ects:
            raise ValidationError('É obrigatório preencher todos os campos do formulário.')

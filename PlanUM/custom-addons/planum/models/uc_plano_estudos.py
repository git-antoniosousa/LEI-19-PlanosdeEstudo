from odoo import fields, models, api
from odoo.exceptions import ValidationError

class UC_Plano_Estudos (models.Model):
    _name = 'planum.uc_plano_estudos'
    _description = 'Unidade Curricular'
    _order = 'ano,semestre asc'
    active = fields.Boolean('Active?', default=True)

    nota = fields.Integer('Nota')
    ano_conclusao = fields.Char('Ano Letivo')
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'ID Plano Estudos')
    uc_plano_curso_id = fields.Many2one('planum.uc_plano_curso', 'UC Plano Curso')
    ano = fields.Selection('Ano', related='uc_plano_curso_id.ano')
    codigo_plano = fields.Char('Código Plano de Curso', related='uc_plano_curso_id.codigo_plano')
    semestre = fields.Selection('Semestre', related='uc_plano_curso_id.semestre')
    fator = fields.Float('Fator', related='uc_plano_curso_id.fator')
    designacao = fields.Char('Designação', related='uc_plano_curso_id.designacao')
    ects = fields.Integer('Créditos ECTS', related='uc_plano_curso_id.ects')
    obrigatoria = fields.Boolean('Obrigatória?', related='uc_plano_curso_id.obrigatoria')

    @api.constrains('nota')
    def uc_plano_estudos_check(self):
        if self.nota:
            if self.nota < 10 or self.nota > 20:
                raise ValidationError('Deve ser atribuída uma nota entre 10 e 20 valores.')

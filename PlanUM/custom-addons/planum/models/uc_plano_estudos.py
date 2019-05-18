from odoo import fields, models

class UC_Plano_Estudos (models.Model):
    _name = 'planum.uc_plano_estudos'
    _description = 'Unidade Curricular'
    _order = 'ano_conclusao asc'
    active = fields.Boolean('Active?', default=True)

    nota = fields.Integer('Nota')
    ano_conclusao = fields.Integer('Ano de Conclusão')
    plano_estudos_id = fields.Many2one('planum.plano_estudos', 'ID Plano Estudos')
    uc_plano_curso_id = fields.Many2one('planum.uc_plano_curso', 'UC Plano Curso')
    ano = fields.Selection('Ano', related='uc_plano_curso_id.ano')
    semestre = fields.Selection('Semestre', related='uc_plano_curso_id.semestre')
    fator = fields.Float('Fator', related='uc_plano_curso_id.fator')
    designacao = fields.Char('Designação', related='uc_plano_curso_id.designacao')
    ects = fields.Integer('Créditos ECTS', related='uc_plano_curso_id.ects')
    obrigatoria = fields.Boolean('Obrigatória?', related='uc_plano_curso_id.obrigatoria')
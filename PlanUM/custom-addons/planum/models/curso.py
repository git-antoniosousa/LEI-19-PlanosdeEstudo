from odoo import fields, models

class Curso(models.Model):
    _name = 'planum.curso'
    _description = 'Curso'
    _order = 'designacao asc'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código Curso')
    designacao = fields.Char('Designação')
    tipo = fields.Char('Tipo Curso')
    alunos=fields.One2many('planum.aluno', 'curso_id', 'Alunos')
    planos_curso = fields.One2many('planum.plano_curso', 'curso_id', 'Planos de Curso')
    direcao_curso = fields.One2many('planum.direcao_curso', 'curso_id', 'Direção de Curso')
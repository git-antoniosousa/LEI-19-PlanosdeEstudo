from odoo import fields, models

class Direcao_Curso(models.Model):
    _name = 'planum.direcao_curso'
    _description = 'Direção de Curso'
    _order = 'codigo desc'
    active = fields.Boolean('Active?', default=True)

    codigo=fields.Char('Código')
    docentes = fields.Many2many('planum.docente', 'direcao_curso_id', 'Docentes')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')
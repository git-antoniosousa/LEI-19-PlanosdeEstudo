from odoo import fields, models, api

class Direcao_Curso(models.Model):
    _name = 'planum.direcao_curso'
    _description = 'Direção de Curso'
    _order = 'codigo desc'
    active = fields.Boolean('Active?', default=True)

    codigo=fields.Char('Código')
    docentes = fields.Many2many('planum.docente', string='Docentes')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')

    #@api.onchange('docentes')
    def adicionar_docente(self):
        security_group = self.env.ref('planum.planum_group_direcao_curso')
        for docente in self.docentes:
            security_group.write({
                'users': [(4, docente.user_id.id)]
            })
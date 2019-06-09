from odoo import fields, models, api
import sys
from odoo.exceptions import ValidationError

class Direcao_Curso(models.Model):
    _name = 'planum.direcao_curso'
    _description = 'Direção de Curso'
    _order = 'codigo desc'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código')
    docentes = fields.Many2many('planum.docente', string='Docentes')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')

    @api.model
    def create(self, vals):
        new_record = super().create(vals)
        security_group = self.env.ref('planum.planum_group_direcao_curso')
        for docente_id in vals['docentes'][0][2]:
            docente = self.env['planum.docente'].browse(docente_id)
            security_group.write({
                'users': [(4, docente.user_id.id)]
            })
        return new_record

    @api.multi
    def write(self, vals):
        security_group = self.env.ref('planum.planum_group_direcao_curso')
        #Remove docentes antigos
        for docente_old in self.docentes:
            sys.stdout.write(str(len(docente_old.direcoes_curso)))
            if len(docente_old.direcoes_curso) <= 1:
                security_group.write({
                    'users': [(3, docente_old.user_id.id)]
                })
        #Adiciona novos docentes
        if 'docentes' in vals:
            for docente_id in vals['docentes'][0][2]:
                docente = self.env['planum.docente'].browse(docente_id)
                security_group.write({
                    'users': [(4, docente.user_id.id)]
                })
        return super().write(vals)

    @api.constrains('codigo', 'curso_id')
    def direcao_curso_check(self):
        # Verificar campos obrigatórios
        if not self.codigo or not self.curso_id:
            raise ValidationError('O código e o curso são campos obrigatórios.')

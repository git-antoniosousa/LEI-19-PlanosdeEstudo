from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Direcao_Curso(models.Model):
    _name = 'planum.direcao_curso'
    _description = 'Direção de Curso'
    _order = 'codigo desc'
    _rec_name = 'codigo'
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
        security_group_direcao_curso = self.env.ref('planum.planum_group_direcao_curso')
        security_group_docente = self.env.ref('planum.planum_group_docente')

        if 'docentes' in vals:
            lista_ids_antiga = [d.user_id.id for d in self.docentes]
            lista_ids_nova = [self.env['planum.docente'].browse(d).user_id.id for d in vals['docentes'][0][2]]

            # Não permitir que o docente se remova a ele próprio
            if self._uid not in lista_ids_nova and self._uid in lista_ids_antiga:
                raise ValidationError('Não é possível remover-se a si próprio da Direção de Curso. Contacte o '
                                      'Administrador para este efeito.')

            docentes_remover = [d for d in self.docentes if d.user_id.id not in lista_ids_nova]
            docentes_ids_adicionar = [d for d in lista_ids_nova if d not in lista_ids_antiga]

            # Remover docentes antigos
            for docente in docentes_remover:
                if len(docente.direcoes_curso) <= 1:
                    security_group_direcao_curso.write({
                        'users': [(3, docente.user_id.id)]
                    })
                    security_group_docente.write({
                        'users': [(4, docente.user_id.id)]
                    })

            # Adicionar novos docentes
            for docente_id in docentes_ids_adicionar:
                security_group_direcao_curso.write({
                    'users': [(4, docente_id)]
                })
                security_group_docente.write({
                    'users': [(3, docente_id)]
                })

        return super().write(vals)

    @api.constrains('codigo', 'curso_id')
    def direcao_curso_check(self):
        # Verificar campos obrigatórios
        if not self.codigo or not self.curso_id:
            raise ValidationError('O código e o curso são campos obrigatórios.')

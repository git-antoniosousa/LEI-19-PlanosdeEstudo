from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Docente(models.Model):
    _inherits = {'res.users': 'user_id'}
    _name = 'planum.docente'
    _description = 'Docente'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    nr_mecanografico = fields.Char('Nº Mecanográfico')
    ucs = fields.Many2many('planum.uc_plano_curso',string='UnidadesCurriculares')
    direcoes_curso = fields.Many2many('planum.direcao_curso', string='DirecoesCurso')

    @api.model
    def create(self, vals):
        # Verificar email
        if not vals['email']:
            raise ValidationError('O nome, o email e o nº mecanográfico são campos obrigatórios.')

        vals['login'] = vals['email']
        new_record = super().create(vals)
        security_group = self.env.ref('planum.planum_group_docente')
        security_group.write({
            'users': [(4,new_record.user_id.id)]
        })
        return new_record

    @api.constrains('email', 'nr_mecanografico')
    def docente_check(self):
        if not self.email or not self.nr_mecanografico:
            raise ValidationError('O nome, o email e o nº mecanográfico são campos obrigatórios.')

        # Não podem existir docentes com nºs mecanográficos iguais
        docentes = self.env['planum.docente'].search([('nr_mecanografico', '=', self.nr_mecanografico)])

        count = 0
        for d in docentes:
            count += 1

        if count > 1:
            raise ValidationError('O nº mecanográfico introduzido já está associado a outro docente. Por favor '
                                  'introduza um nº mecanográfico diferente.')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True
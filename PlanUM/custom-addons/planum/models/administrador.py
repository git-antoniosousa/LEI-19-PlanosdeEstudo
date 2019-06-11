from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Administrador(models.Model):
    _inherits = {'res.users': 'user_id'}
    _name = 'planum.administrador'
    _description = 'Administrador'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)
    nr_mecanografico = fields.Char('Nº Mecanográfico')

    @api.model
    def create(self, vals):
        # Verificar nº mecanográfico
        if not vals['nr_mecanografico']:
            raise ValidationError('É obrigatório preencher todos os campos do formulário.')

        vals['login'] = vals['nr_mecanografico']

        # Arranjar maneira de dar password?
        vals['password'] = vals['nr_mecanografico']
        new_record = super().create(vals)
        security_group = self.env.ref('planum.planum_group_admin')
        security_group.write({
            'users': [(4, new_record.user_id.id)]
        })
        return new_record

    @api.constrains('nr_mecanografico')
    def administrador_check(self):
        # Verificar campos obrigatórios
        if not self.nr_mecanografico:
            raise ValidationError('O nome e o nº mecanográfico são campos obrigatórios.')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True
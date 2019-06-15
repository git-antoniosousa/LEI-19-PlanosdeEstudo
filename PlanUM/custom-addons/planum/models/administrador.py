from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Administrador(models.Model):
    _inherits = {'res.users': 'user_id'}
    _name = 'planum.administrador'
    _description = 'Administrador'
    _order = 'name desc'
    active = fields.Boolean('Active?', default=True)

    @api.model
    def create(self, vals):
        # Verificar email
        if not vals['email']:
            raise ValidationError('É obrigatório preencher todos os campos do formulário.')

        vals['login'] = vals['email']

        new_record = super().create(vals)
        security_group = self.env.ref('planum.planum_group_admin')
        security_group.write({
            'users': [(4, new_record.user_id.id)]
        })
        return new_record

    @api.constrains('email')
    def administrador_check(self):
        if not self.email:
            raise ValidationError('O email e o nome são campos obrigatório.')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True

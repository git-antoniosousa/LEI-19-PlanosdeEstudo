from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Plano_Curso(models.Model):
    _name = 'planum.plano_curso'
    _description = 'Plano de Curso'
    _order = 'data_inicio desc'
    _rec_name = 'curso_id'
    active = fields.Boolean('Active?', default=True)

    data_inicio=fields.Date('Data Inicio')
    data_fim = fields.Date('Data Fim')
    curso_id = fields.Many2one('planum.curso', 'Curso ID')
    ucs = fields.One2many('planum.uc_plano_curso', 'plano_curso_id', 'Unidades Curriculares')


    @api.constrains('data_inicio','data_fim', 'ucs', 'curso_id')
    def plano_curso_check(self):
        # Verificar se foram definidas datas de início e fim
        if not self.data_inicio or not self.data_fim or not self.curso_id:
            raise ValidationError(
                'O plano de curso deve ter datas de início e fim devidamente definidas.')

        elif not self.ucs:
            raise ValidationError(
                'O plano de curso deve conter pelo menos uma UC.')

        # Verificar se as datam são posteriores ou iguais à data atual
        elif self.data_inicio < fields.Date.today() or self.data_fim < fields.Date.today():
            raise ValidationError(
                'As datas de início e fim de um plano de curso não podem ser anteriores à data atual.')

        # Verificar se a data de início é anterior à de fim
        elif self.data_inicio >= self.data_fim:
            raise ValidationError(
                'A data de fim deve ser posterior à data de início.')

        # Verificar se não existem planos de curso com datas coincidentes
        planos_curso = self.env['planum.plano_curso'].search([('data_inicio', '>=', str(fields.Date.today())),
                                                              ('id', '!=', self.id),
                                                              ('curso_id', '=', self.curso_id.id)])

        for plano in planos_curso:
            if self.data_inicio <= plano.data_fim:
                curso = self.env['planum.curso'].browse(self.curso_id.id)
                raise ValidationError(
                    'Já existe um plano de curso definido de ' + str(plano.data_inicio) + ' a ' + str(plano.data_fim) +
                    ', para o curso ' + str(curso.codigo) + '. Não pode existir mais do que um plano de curso na '
                    'mesma data.')

    @api.one
    def desativar(self):
        self.active = False

    @api.one
    def ativar(self):
        self.active = True

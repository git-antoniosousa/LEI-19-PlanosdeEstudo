from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Curso(models.Model):
    _name = 'planum.curso'
    _description = 'Curso'
    _order = 'designacao asc'
    _rec_name = 'designacao'
    active = fields.Boolean('Active?', default=True)

    codigo = fields.Char('Código Curso')
    designacao = fields.Char('Designação')
    tipo = fields.Selection([(1,'Licenciatura'),(2,'Mestrado Integrado'),(3,'Mestrado')], default=1)
    alunos = fields.One2many('planum.aluno', 'curso_id', 'Alunos')
    planos_curso = fields.One2many('planum.plano_curso', 'curso_id', 'Planos de Curso')
    direcao_curso = fields.One2many('planum.direcao_curso', 'curso_id', 'Direção de Curso')

    @api.one
    def plano_atual(self):
        max_date = None
        plano_atual = None

        # Verificar se existe algum plano de curso
        if not self.planos_curso:
            return None

        # Verificar se o plano ainda não expirou
        for plano in self.planos_curso:
            if not max_date or plano.data_fim >= max_date:
                max_date = plano.data_fim
                plano_atual = plano.id

        if max_date < fields.Date.today():
            return None
        else:
            return plano_atual

    @api.one
    def desativar(self):
        self.active=False

    @api.one
    def ativar(self):
        self.active = True

    @api.constrains('codigo', 'designacao')
    def curso_check(self):
        # Verificar campos obrigatórios
        if not self.codigo or not self.designacao:
            raise ValidationError('O código do curso e a designação são campos obrigatórios.')
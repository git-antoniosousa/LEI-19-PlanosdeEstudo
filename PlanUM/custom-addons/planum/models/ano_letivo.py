from odoo import fields, models, api

class Ano_Letivo(models.Model):
    _name = 'planum.ano_letivo'
    _description = 'Ano Letivo'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')

    def mudanca_ano(self):
        self.guarda_historico()

    def guarda_historico(self):
        cursos = self.env['planum.curso'].search([])
        estatistica = self.env['planum.estatistica']
        for curso in cursos:
            plano_atual_id = curso.plano_atual()[0]
            plano_atual = self.env['planum.plano_curso'].browse(plano_atual_id)
            #TODO: Verificar se há plano
            for uc in plano_atual.ucs:
                estatistica.create({
                    'ano': self.ano,
                    'aprovados': uc.aprovados,
                    'reprovados': uc.reprovados,
                    'uc_plano_curso_id': uc.id
                })

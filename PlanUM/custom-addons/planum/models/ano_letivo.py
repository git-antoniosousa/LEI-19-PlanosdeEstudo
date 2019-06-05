from odoo import fields, models, api

class Ano_Letivo(models.Model):
    _name = 'planum.ano_letivo'
    _description = 'Ano Letivo'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')
    previsoes = fields.One2many('planum.previsao', 'ano_letivo_id', 'Previsões')

    def proximo_ano(self):
        ano_int = int(self.ano[0:4])
        ano_int+=1
        return str(ano_int) + "/" + str(ano_int+1)


    def mudanca_ano(self):
        self.guarda_historico()
        self.alterar_planos_estudo()
        self.previsao()
        self.ano=self.proximo_ano()

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

    def alterar_planos_estudo (self):
        #Isto não vai buscar desativados?
        alunos = self.env['planum.aluno'].search([])
        fator = 5
        for aluno in alunos:
            creditos_totais=0
            creditos_feitos=0
            for uc in aluno.plano_estudos_id.ucs:
                if uc.ano_conclusao == self.ano:
                    creditos_totais+=uc.ects
                    if uc.nota >=10:
                        creditos_feitos += uc.ects
                    #Fazer isto na previsão?
                    else:
                        uc.ano_conclusao=self.proximo_ano()

            if creditos_feitos>=(creditos_totais-fator):
                aluno.ano+=1

    def previsao(self):
        return

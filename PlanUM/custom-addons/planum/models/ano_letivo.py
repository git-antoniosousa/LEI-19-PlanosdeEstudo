from odoo import fields, models, api
import sys

class Ano_Letivo(models.Model):
    _name = 'planum.ano_letivo'
    _description = 'Ano Letivo'
    active = fields.Boolean('Active?', default=True)

    ano = fields.Char('Ano')

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
        #TODO Mudar para 60
        fator = 60
        for aluno in alunos:
            creditos_totais=0
            creditos_feitos=0
            for uc in aluno.plano_estudos_id.ucs:
                if uc.ano_conclusao == self.ano:
                    creditos_totais+=uc.ects
                    if uc.nota >=10:
                        creditos_feitos += uc.ects
                    else:
                        uc.nota=0

            if creditos_feitos>=(creditos_totais-fator):
                sys.stdout.write("Passou de ano!\n\n" + str(creditos_feitos) + "/" + str(creditos_totais) + "\n\n")
                aluno.ano+=1

    def previsao(self):
        alunos = self.env['planum.aluno'].search([])
        cursos = self.env['planum.curso'].search([])
        previsao = self.env['planum.previsao']

        for curso in cursos:
            plano_atual_id = curso.plano_atual()[0]
            plano_atual = self.env['planum.plano_curso'].browse(plano_atual_id)
            # TODO: Verificar se há plano
            for uc in plano_atual.ucs:
                previsao.create({
                    'ano': self.proximo_ano(),
                    'possiveis': 0,
                    'garantidas': 0,
                    'uc_plano_curso_id': uc.id
                })


        for aluno in alunos:
            for uc in aluno.plano_estudos_id.ucs:
                creditos_atrasados=0
                previsao_atual = uc.uc_plano_curso_id.previsao_atual()
                #Cadeira atrasada
                if uc.ano < aluno.ano and uc.nota < 10 and uc.ano_conclusao == self.ano:
                    previsao_atual.possiveis+=1
                    previsao_atual.garantidas += 1
                    sys.stdout.write("Cadeira atrasada\n" + str(previsao_atual.possiveis) + "/" + str(previsao_atual.garantidas) + ":" + str(previsao) + "\n\n")
                    creditos_atrasados+=uc.ects
                    #uc.ano_conclusao=self.proximo_ano()
                #Cadeiras do ano
                elif uc.ano == aluno.ano and uc.nota < 10:
                    if creditos_atrasados <= 15:
                        previsao_atual.possiveis += 1
                        previsao_atual.garantidas += 1
                    else:
                        previsao_atual.possiveis += 1
                    sys.stdout.write("Cadeira do ano\n" + str(previsao_atual.possiveis) + "/" + str(previsao_atual.garantidas) + ":" + str(previsao) + "\n\n")
                    #uc.ano_conclusao = self.proximo_ano()

        return

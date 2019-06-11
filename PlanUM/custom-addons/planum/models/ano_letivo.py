from odoo import fields, models, api
import sys
import re
from odoo.exceptions import ValidationError

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
        reprovados=self.alterar_planos_estudo()
        self.previsao(reprovados)
        self.ano=self.proximo_ano()

    def guarda_historico(self):
        cursos = self.env['planum.curso'].search([])
        estatistica = self.env['planum.estatistica']
        for curso in cursos:
            plano_curso_id = curso.plano_atual()[0]

            # Verificar se existe plano de curso ativo
            if plano_curso_id:
                plano_curso = self.env['planum.plano_curso'].browse(plano_curso_id)
                for uc in plano_curso.ucs:
                    estatistica.create({
                        'ano': self.ano,
                        'aprovados': uc.aprovados,
                        'reprovados': uc.reprovados,
                        'uc_plano_curso_id': uc.id
                    })

    def alterar_planos_estudo (self):
        alunos = self.env['planum.aluno'].search([])
        fator = 30
        reprovados = []
        for aluno in alunos:
            creditos_totais = 0
            creditos_feitos = 0
            for uc in aluno.plano_estudos_id.ucs:
                if uc.ano_conclusao == self.ano:
                    creditos_totais += uc.ects
                    if uc.nota >= 10:
                        creditos_feitos += uc.ects
                    else:
                        uc.nota = 0

            if creditos_feitos >= (creditos_totais-fator):
                sys.stdout.write("Passou de ano!\n" + str(creditos_feitos) + "/" + str(creditos_totais) + "\n\n")
                aluno.ano += 1
            else:
                reprovados.append(aluno.nr_mecanografico)
        return reprovados

    def previsao(self, reprovados):
        alunos = self.env['planum.aluno'].search([])
        cursos = self.env['planum.curso'].search([])
        previsao = self.env['planum.previsao']
        prev = {}

        for curso in cursos:
            plano_curso_id = curso.plano_atual()[0]

            # Verificar se existe plano de curso ativo
            if plano_curso_id:
                plano_curso = self.env['planum.plano_curso'].browse(plano_curso_id)
                for uc in plano_curso.ucs:
                    prev[uc.designacao] =previsao.create({
                        'ano': self.proximo_ano(),
                        'min': 0,
                        'med': 0,
                        'max': 0,
                        'uc_plano_curso_id': uc.id
                    })

        for aluno in alunos:
            sys.stdout.write("Aluno " + str(aluno.nr_mecanografico) + "\n")
            creditos_atrasados = 0
            cadeiras_atrasadas = 0
            creditos=60
            # Percorrer UCs por ordem
            for uc in sorted(aluno.plano_estudos_id.ucs, key=lambda uc: uc.ano):
                previsao_atual = prev[uc.designacao]
                # Cadeira atrasada
                if uc.ano < aluno.ano and uc.nota < 10 and uc.ano_conclusao == self.ano:
                    previsao_atual.min+=1
                    previsao_atual.med+= 1
                    previsao_atual.max+= 1
                    sys.stdout.write("Cadeira atrasada " + uc.designacao + " \n" + str(previsao_atual.min) + "/" + str(previsao_atual.max) + ":" + str(previsao) + "\n\n")
                    creditos_atrasados+=uc.ects
                    cadeiras_atrasadas+=1
                    creditos-=uc.ects
                    uc.ano_conclusao=self.proximo_ano()
                # Cadeiras do ano
                elif uc.ano == aluno.ano and uc.nota < 10:
                    if creditos_atrasados <= 15:
                        previsao_atual.min += 1
                        previsao_atual.med += 1
                        previsao_atual.max += 1
                        creditos -= uc.ects
                    else:
                        previsao_atual.max += 1
                        creditos -= uc.ects
                        previsao_atual.med += cadeiras_atrasadas/12
                    sys.stdout.write("Cadeira do ano " + uc.designacao + " \n" + str(previsao_atual.min) + "/" + str(previsao_atual.max) + ":" + str(previsao) + "\n\n")
                    uc.ano_conclusao = self.proximo_ano()
                elif uc.ano == aluno.ano+1 and aluno.nr_mecanografico in reprovados and creditos > 0:
                    previsao_atual.max += 1
                    previsao_atual.med += (creditos/5) / 12

        return

    @api.model_cr
    def init(self):
        # Criar ano letivo caso não exista ao inicializar
        anos_letivos = self.env['planum.ano_letivo'].search([])

        if not anos_letivos:
            data = str(fields.Date.today()).split("-")
            mes = int(data[1])
            ano = int(data[0])

            if 1 <= mes <= 8:
                ano = str(ano - 1) + '/' + str(ano)
            else:
                ano = str(ano) + '/' + str(ano + 1)

            self.env['planum.ano_letivo'].create({
                'ano': ano
            })

    @api.constrains('ano')
    def ano_check(self):
        # Só pode existir um ano letivo
        anos_letivos = self.env['planum.ano_letivo'].search([])

        count = 0
        ano_atual = 0
        for ano in anos_letivos:
            count += 1

            if count == 1:
                ano_atual = ano.ano

        if count > 1:
            raise ValidationError('Não é possível criar um ano letivo novo porque o ano letivo ' + ano_atual +
                                  ' está a decorrer.')

        # Verificar campos obrigatórios
        if not self.ano:
            raise ValidationError('O ano é um campo obrigatório.')

        # Verificar formato do ano letivo
        check = re.search("[0-9]{4}/[0-9]{4}", self.ano)
        if not check:
            raise ValidationError('O ano letivo deve seguir o seguinte formato: 2010/2011.')

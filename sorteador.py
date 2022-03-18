from time import sleep
from random import randint
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4
from pathlib import Path


class SortearMegasena:

    def __init__(self):
        self.jogos = 0


    def mp(self, mm):
        return mm/0.352777

    def validarInput(self):
        print('-' * 40)
        print(f'{"SORTEADOR DE NUMEROS PARA MEGA-SENA":^40}')
        print('-' * 40)
        
        dezenasArray = ['','','','','','']    
        for x in range(0, 6, 1):
            while True:
                try:
                    inputUser = int(input(f'Entre com a {x + 1}° dezena: '))
                    if inputUser in dezenasArray:
                        inputUser = int(input(f'Dezena {inputUser} inserida anteriormente, escolha uma diferente: '))
                    while inputUser < 1 or inputUser > 60:
                        inputUser = int(input(f'Digite um valor entre 01 e 60 para a {x + 1}° dezena: '))
                except ValueError:
                    print('Digite um valor entre 01 e 60')
                    continue
                else:
                    dezenasArray[x] = inputUser
                    break

        dezenasArray.sort()
        print(dezenasArray)

        qtd_jogos = int(input('Quantos jogos deseja sortear? '))
        while qtd_jogos < 1 or qtd_jogos > 99:
            qtd_jogos = int(input('Escolha um valor entre 01 e 99 para a quantidade de jogos: '))
        self.jogos = qtd_jogos

        return dezenasArray



    def printPdf(self):
        dezenasArray = self.validarInput()

        dataAtual = datetime.today().strftime('%Y-%m-%d-%H-%M')
        dataNoFormat = datetime.today().strftime('%d/%m/%Y %H:%M')
        filtro = 2
        print('Processando...')
        sleep(3)
        
        print(' - ' * 40)
        x = self.mp(210)
        pastaApp = str(Path.home() / "Downloads")

        nome_pdf = f'sorteador_megasena_{dataAtual}'
        pdf = canvas.Canvas('{}/{}.pdf'.format(pastaApp,nome_pdf), pagesize=A4)
        pdf.drawString(self.mp(50),self.mp(250), '-' * 95)
        pdf.drawString(self.mp(50),self.mp(245), f'{"SORTEADOR DE NUMEROS PARA MEGA-SENA":^40}')
        pdf.drawString(self.mp(50),self.mp(240), '-' * 95)
        pdf.drawString(self.mp(50),self.mp(235), 'Dezena escolhida: {:02d} - {:02d} - {:02d} - {:02d} - {:02d} - {:02d}  | Data: {}'.format(dezenasArray[0], dezenasArray[1], dezenasArray[2], dezenasArray[3], dezenasArray[4], dezenasArray[5], dataNoFormat))
        pdf.drawString(self.mp(50),self.mp(230), '-' * 95)
        pdf.drawString(self.mp(50),self.mp(225), f'Margem do filtro para mais ou para menos: {filtro}')
        pdf.drawString(self.mp(50),self.mp(220), '(Filtro aumentará conforme proximidade dos números)')

        arrayResult = ['','','','','','']
        for jogo in range(0, self.jogos, 1):
            for z in range(0 , 6, 1):
                randNumber = randint((dezenasArray[z] - filtro), (dezenasArray[z] + filtro))
                countWhile = 0
                while True:
                    if randNumber < 1:
                        randNumber = 1
                    elif randNumber > 60:
                        randNumber = 60
                    elif randNumber in arrayResult:
                        randNumber = randint((dezenasArray[z] - filtro), (dezenasArray[z] + filtro))
                    else:
                        break
                    countWhile += 1
                    if countWhile > 10:
                        filtro = 3
                    if countWhile > 20:
                        filtro = 4
                    if countWhile > 30:
                        filtro = 5
                arrayResult[z] = randNumber

            arrayResult.sort()
            print(f'Números do {jogo + 1}° jogo: {arrayResult[0]:02d}-{arrayResult[1]:02d}-{arrayResult[2]:02d}-{arrayResult[3]:02d}-{arrayResult[4]:02d}-{arrayResult[5]:02d}')
            print('-' * 40)
            x -= self.mp(10)
            pdf.drawString(self.mp(50),x, 'Números do {}° jogo : {:02d} - {:02d} - {:02d} - {:02d} - {:02d} - {:02d}'.format(jogo + 1,arrayResult[0], arrayResult[1], arrayResult[2], arrayResult[3], arrayResult[4], arrayResult[5]))
            pdf.drawString(self.mp(50),x - self.mp(5), '-' * 65)
            pdf.setTitle(nome_pdf)
            if x < 60:
                pdf.showPage()
                x = self.mp(250)

        pdf.save()
        print(f'Foi criado o arquivo PDF em {pastaApp}')
        while True:
            try:
                inputUser = str(input(f'Pressione Y para encerrar: ')).upper()
                if inputUser == 'Y':
                    break
            except ValueError:
                inputUser = str(input(f''))
                continue
            
       
        

megasena = SortearMegasena()
megasena.printPdf()
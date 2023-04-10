import tkinter as tk
from random import sample
import itertools as it


class Mastermind(tk.Frame):
    #SETANDO AS CONFIGURACOES PRINCIPAIS DO JOGO
    def __init__(self, master, linhas=4, cores=6, tentativas=12, bg="white", fg="black", **kwargs):
        self.numbLinhas = linhas
        self.numbCores = cores
        self.numbTentativas = tentativas
        self.bg = bg 
        self.fg = fg
        self.master = master
        self.listaCores = ["#9E5D00", "#FF0000", "#FF7F00", "#FFFF00", "#00FF00",
                        "#0000FF", "#FF00FF", "#8C44FF", "#FFFFFF", "#000000"][:self.numbCores]
        self.reseta_ciclo()
        #sorteia resposta correta
        self.respostaCorreta = sample(self.listaCores, k=self.numbLinhas)
        super().__init__(self.master, bg=self.bg, **kwargs)
        print(self.respostaCorreta)
        self.cria_interface()

    #CRIANDO A INTERFACE DO JOGO
    def cria_interface(self):
        self.allTentativas = [tk.Frame(self, bg=self.bg) for _ in range(self.numbTentativas)]
        self.allMarcacoes = [tk.Frame(self, bg=self.bg) for _ in range(self.numbTentativas)]
        self.respostaFrame = tk.Frame(self, bg=self.bg)
        self.respostaCobrir = tk.Frame(self, bg=self.fg, relief=tk.RAISED)
        #QUADRADOS QUE SERAO ESCOLHIDAS AS CORES
        self.allTentativasPins = [[tk.Label(self.allTentativas[i], width=2, height=1, bg="grey", relief=tk.SUNKEN)
                             for _ in range(self.numbLinhas)]
                             for i in range(self.numbTentativas)]
        #QUADRADOS QUE VERICARAO SE AS CORES ESTAO CORRETAS
        self.allMarcacoesPins = [[tk.Label(self.allMarcacoes[i], width=1, height=1, bg="lightgrey", relief=tk.SUNKEN)
                             for _ in range(self.numbLinhas)]
                             for i in range(self.numbTentativas)]
        self.respostaPins = [tk.Label(self.respostaFrame, width=2, height=1, bg=colour, relief=tk.RAISED) for colour in self.respostaCorreta]
        self.botaoVerificar = tk.Button(self, text="VERIFICAR", command=self.prox_tentativa, bg=self.bg, fg=self.fg)
        self.tentativasAtivas = 0

        for rowIndex in range(self.numbTentativas):
            for holeIndex in range(self.numbLinhas):
                self.allTentativasPins[rowIndex][holeIndex].grid(row=0, column=holeIndex, padx=1, pady=4)
                self.allMarcacoesPins[rowIndex][holeIndex].grid(row=0, column=holeIndex, padx=1, pady=4)
            tk.Label(self, text=str(rowIndex+1), bg=self.bg, fg=self.fg).grid(row=self.numbTentativas-rowIndex, column=0)
            self.allTentativas[rowIndex].grid(row=rowIndex+1, column=1)
            self.allMarcacoes[rowIndex].grid(row=rowIndex+1, column=3)

        for i, a in enumerate(self.respostaPins):
            a.grid(row=0, column=i, padx=1)
        #COBRE A RESPOSTA
        tk.Label(self, text="   ", bg=self.bg).grid(row=0, column=2)
        tk.Label(self, text="   ", bg=self.bg).grid(row=0, column=4)
        for a in [tk.Label(self.respostaCobrir, width=2, height=1, bg=self.fg) for _ in range(self.numbLinhas)]:
            a.pack(side=tk.LEFT, padx=1)

        self.respostaCobrir.grid(row=0, column=1, pady=15)
        self.botaoVerificar.grid(column=1, row=999, pady=10)
        self.prox_tentativa(start=True)


    def prox_tentativa(self, start=False):
        # Check there are no blanks
        for colour in self.get_pin_colours():
            if colour == "grey" and not start:
                return None

        # Stop responding to mouse button and remove highlighting
        self.reseta_ciclo()
        self.allTentativas[self.tentativasAtivas].config(bg=self.bg)
        for pin in self.allTentativasPins[self.tentativasAtivas]:
            pin.unbind("<1>")
            pin["cursor"] = ""

        # Add the mark pins for the guess
        score = self.score_tentativas(self.get_pin_colours(), self.respostaCorreta)
        if not start and len(score) != 0:
            score = self.score_tentativas(self.get_pin_colours(), self.respostaCorreta)
            for i, pin in enumerate(self.allMarcacoesPins[self.tentativasAtivas]):
                if i > len(score)-1:
                    break
                pin.config(bg=score[i], relief=tk.RAISED)

        # CHECA SE GANHOU
        if score == ["Black" for _ in range(self.numbLinhas)]:
            self.respostaCobrir.grid_forget()
            self.respostaFrame.grid(row=0, column=1, pady=15)
            self.botaoVerificar["command"] = None
            return None

        # MOVE PARA CIMA PARA O JOGO CONTINUAR NUMA NOVA TENTATIVA
        try:
            self.tentativasAtivas -= 1
            self.allTentativas[self.tentativasAtivas].config(bg=self.fg)
            for i, pin in enumerate(self.allTentativasPins[self.tentativasAtivas]):
                pin.bind("<1>", lambda event, i=i: self.change_pin_colour(event, i))
                pin["cursor"] = "hand"
        except IndexError:
            raise NotImplementedError()
            # add lose condition
            # Checa se o jogador já usou todas as suas tentativas e, se sim, mostra a sequência correta
        if self.tentativasAtivas >= self.numbTentativas:
            self.respostaCobrir.grid_forget()
            self.respostaFrame.grid(row=0, column=1, pady=15)
            self.botaoVerificar["command"] = None
            for i, pin in enumerate(self.respostaPins):
                pin.config(bg=self.respostaCorreta[i])
                


    @staticmethod
    def score_tentativas(guess, respostaCorreta):
        respostaCorreta = respostaCorreta.copy()
        blacks = ["Black" for secret, guess_item in zip(respostaCorreta, guess) if secret == guess_item]
        whites = []
        for guess_item in guess:
            if guess_item in respostaCorreta:
                respostaCorreta[respostaCorreta.index(guess_item)] = None
                whites.append("White")
        return blacks + whites[:-len(blacks)]
    

    def get_pin_colours(self):
        return [pin["bg"] for pin in self.allTentativasPins[self.tentativasAtivas]]

    def change_pin_colour(self, event, i):
        event.widget.config(bg=next(self.colourCycles[i]), relief=tk.RAISED)

    def reseta_ciclo(self):
        self.colourCycles = it.tee(it.cycle(self.listaCores), self.numbLinhas)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Mastermind")
    x = Mastermind(window)
    x.pack()
    window.mainloop()
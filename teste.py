"""
==============================================================================
 GERENCIADOR DE CAMPEONATO DE XADREZ
 Disciplina: Estrutura de Dados
 Integrantes: (preencher nomes aqui - 3 a 5 integrantes)
==============================================================================

Este projeto implementa um sistema de gerenciamento de um campeonato de
xadrez utilizando 4 estruturas de dados clássicas, todas implementadas
"na mão" (do zero, sem usar list/deque prontos do Python como estrutura
principal):

    1. VETOR          -> classe Vetor            (armazena os jogadores cadastrados)
    2. LISTA ENCADEADA -> classe ListaEncadeada   (armazena o histórico de partidas)
    3. FILA (FIFO)     -> classe Fila             (fila de espera para a próxima rodada)
    4. PILHA (LIFO)    -> classe Pilha            (permite desfazer a última partida)

O programa roda em modo texto (CLI), com um menu interativo, ideal para
demonstração ao vivo em sala de aula.

Como executar:
    python gerenciador_campeonato_xadrez.py
==============================================================================
"""

import os
import time


# =============================================================================
# 1) VETOR  -----------------------------------------------------------------
# =============================================================================
class Vetor:
    """
    Implementação manual de um Vetor (array dinâmico), semelhante a um
    ArrayList: quando enche, dobra de tamanho (redimensionamento).

    Usado para armazenar todos os jogadores cadastrados no campeonato.
    """

    def __init__(self, capacidade_inicial=4):
        self._dados = [None] * capacidade_inicial
        self._capacidade = capacidade_inicial
        self._tamanho = 0

    def _redimensionar(self):
        nova_capacidade = self._capacidade * 2
        novo_array = [None] * nova_capacidade
        for i in range(self._tamanho):
            novo_array[i] = self._dados[i]
        self._dados = novo_array
        self._capacidade = nova_capacidade

    def adicionar(self, item):
        if self._tamanho == self._capacidade:
            self._redimensionar()
        self._dados[self._tamanho] = item
        self._tamanho += 1

    def remover_por_indice(self, indice):
        if indice < 0 or indice >= self._tamanho:
            raise IndexError("Índice fora do intervalo do vetor.")
        item = self._dados[indice]
        for i in range(indice, self._tamanho - 1):
            self._dados[i] = self._dados[i + 1]
        self._dados[self._tamanho - 1] = None
        self._tamanho -= 1
        return item

    def obter(self, indice):
        if indice < 0 or indice >= self._tamanho:
            raise IndexError("Índice fora do intervalo do vetor.")
        return self._dados[indice]

    def buscar_por_nome(self, nome):
        """Busca linear (O(n)) por um jogador pelo nome (case-insensitive)."""
        for i in range(self._tamanho):
            jogador = self._dados[i]
            if jogador.nome.lower() == nome.lower():
                return jogador
        return None

    def esta_vazio(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        for i in range(self._tamanho):
            yield self._dados[i]


# =============================================================================
# 2) LISTA ENCADEADA ----------------------------------------------------------
# =============================================================================
class NoLista:
    """Nó de uma lista encadeada simples."""

    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    """
    Implementação manual de uma Lista Encadeada Simples (singly linked list).

    Usada para armazenar o histórico cronológico de partidas do campeonato
    (cada partida disputada vira um nó no fim da lista).
    """

    def __init__(self):
        self._inicio = None
        self._fim = None
        self._tamanho = 0

    def inserir_fim(self, dado):
        novo_no = NoLista(dado)
        if self._inicio is None:
            self._inicio = novo_no
            self._fim = novo_no
        else:
            self._fim.proximo = novo_no
            self._fim = novo_no
        self._tamanho += 1

    def remover_ultimo(self):
        """Remove e retorna o último elemento inserido (usado pelo 'desfazer')."""
        if self._inicio is None:
            return None

        if self._inicio is self._fim:
            dado = self._inicio.dado
            self._inicio = None
            self._fim = None
            self._tamanho -= 1
            return dado

        # Percorre até o penúltimo nó
        atual = self._inicio
        while atual.proximo is not self._fim:
            atual = atual.proximo

        dado = self._fim.dado
        atual.proximo = None
        self._fim = atual
        self._tamanho -= 1
        return dado

    def esta_vazia(self):
        return self._inicio is None

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self._inicio
        while atual is not None:
            yield atual.dado
            atual = atual.proximo


# =============================================================================
# 3) FILA (FIFO) --------------------------------------------------------------
# =============================================================================
class NoFila:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class Fila:
    """
    Implementação manual de uma Fila (FIFO) usando nós encadeados.

    Usada como fila de espera: jogadores entram na fila para aguardar o
    sorteio da próxima partida. O primeiro que entra é o primeiro a jogar.
    """

    def __init__(self):
        self._inicio = None
        self._fim = None
        self._tamanho = 0

    def enfileirar(self, dado):
        novo_no = NoFila(dado)
        if self._fim is None:
            self._inicio = novo_no
            self._fim = novo_no
        else:
            self._fim.proximo = novo_no
            self._fim = novo_no
        self._tamanho += 1

    def desenfileirar(self):
        if self._inicio is None:
            return None
        dado = self._inicio.dado
        self._inicio = self._inicio.proximo
        if self._inicio is None:
            self._fim = None
        self._tamanho -= 1
        return dado

    def esta_vazia(self):
        return self._inicio is None

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self._inicio
        while atual is not None:
            yield atual.dado
            atual = atual.proximo


# =============================================================================
# 4) PILHA (LIFO) --------------------------------------------------------------
# =============================================================================
class NoPilha:
    def __init__(self, dado):
        self.dado = dado
        self.abaixo = None


class Pilha:
    """
    Implementação manual de uma Pilha (LIFO) usando nós encadeados.

    Usada para permitir "desfazer" a última partida registrada: cada
    resultado registrado é empilhado; ao desfazer, desempilhamos o topo
    e revertemos a pontuação.
    """

    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, dado):
        novo_no = NoPilha(dado)
        novo_no.abaixo = self._topo
        self._topo = novo_no
        self._tamanho += 1

    def desempilhar(self):
        if self._topo is None:
            return None
        dado = self._topo.dado
        self._topo = self._topo.abaixo
        self._tamanho -= 1
        return dado

    def ver_topo(self):
        return self._topo.dado if self._topo is not None else None

    def esta_vazia(self):
        return self._topo is None

    def __len__(self):
        return self._tamanho


# =============================================================================
# ENTIDADES DO DOMÍNIO (Jogador e Partida)
# =============================================================================
class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.pontos = 0.0
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

    def __str__(self):
        return (f"{self.nome:<20} | Pontos: {self.pontos:<5.1f} | "
                f"V:{self.vitorias} E:{self.empates} D:{self.derrotas}")


class Partida:
    def __init__(self, rodada, jogador1, jogador2, resultado):
        """
        resultado:
            1 -> vitória do jogador1
            2 -> vitória do jogador2
            0 -> empate
        """
        self.rodada = rodada
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        self.resultado = resultado

    def descricao(self):
        if self.resultado == 1:
            texto = f"{self.jogador1.nome} venceu {self.jogador2.nome}"
        elif self.resultado == 2:
            texto = f"{self.jogador2.nome} venceu {self.jogador1.nome}"
        else:
            texto = f"{self.jogador1.nome} empatou com {self.jogador2.nome}"
        return f"Rodada {self.rodada}: {texto}"


# =============================================================================
# CLASSE PRINCIPAL: TORNEIO DE XADREZ
# =============================================================================
class TorneioXadrez:
    def __init__(self):
        self.jogadores = Vetor()            # (1) VETOR
        self.historico = ListaEncadeada()   # (2) LISTA ENCADEADA
        self.fila_espera = Fila()           # (3) FILA
        self.pilha_desfazer = Pilha()       # (4) PILHA
        self.rodada_atual = 1

    # ---------------- Jogadores (Vetor) ----------------
    def cadastrar_jogador(self, nome):
        if self.jogadores.buscar_por_nome(nome) is not None:
            print(f"\n Já existe um jogador cadastrado com o nome '{nome}'.")
            return
        jogador = Jogador(nome)
        self.jogadores.adicionar(jogador)
        print(f"\n Jogador '{nome}' cadastrado com sucesso!")

    def listar_jogadores(self):
        if self.jogadores.esta_vazio():
            print("\nNenhum jogador cadastrado ainda.")
            return
        print("\n--- Jogadores cadastrados (armazenados em Vetor) ---")
        for jogador in self.jogadores:
            print(" -", jogador)

    # ---------------- Fila de espera (Fila) ----------------
    def entrar_na_fila(self, nome):
        jogador = self.jogadores.buscar_por_nome(nome)
        if jogador is None:
            print(f"\n Jogador '{nome}' não está cadastrado.")
            return
        self.fila_espera.enfileirar(jogador)
        print(f"\n {nome} entrou na fila de espera.")

    def ver_fila(self):
        if self.fila_espera.esta_vazia():
            print("\nA fila de espera está vazia.")
            return
        print("\n--- Fila de espera (estrutura Fila - FIFO) ---")
        posicao = 1
        for jogador in self.fila_espera:
            print(f" {posicao}º -> {jogador.nome}")
            posicao += 1

    # ---------------- Registrar partida (Fila + Lista + Pilha) ----------------
    def registrar_partida(self, resultado):
        if len(self.fila_espera) < 2:
            print("\n É preciso pelo menos 2 jogadores na fila para registrar uma partida.")
            return None

        jogador1 = self.fila_espera.desenfileirar()
        jogador2 = self.fila_espera.desenfileirar()

        partida = Partida(self.rodada_atual, jogador1, jogador2, resultado)

        # Atualiza pontuação
        if resultado == 1:
            jogador1.pontos += 1
            jogador1.vitorias += 1
            jogador2.derrotas += 1
        elif resultado == 2:
            jogador2.pontos += 1
            jogador2.vitorias += 1
            jogador1.derrotas += 1
        else:
            jogador1.pontos += 0.5
            jogador2.pontos += 0.5
            jogador1.empates += 1
            jogador2.empates += 1

        self.historico.inserir_fim(partida)     # (2) Lista Encadeada
        self.pilha_desfazer.empilhar(partida)   # (4) Pilha
        self.rodada_atual += 1

        print(f"\n Partida registrada: {partida.descricao()}")
        return partida

    # ---------------- Histórico (Lista Encadeada) ----------------
    def ver_historico(self):
        if self.historico.esta_vazia():
            print("\nNenhuma partida registrada ainda.")
            return
        print("\n--- Histórico de partidas (estrutura Lista Encadeada) ---")
        for partida in self.historico:
            print(" -", partida.descricao())

    # ---------------- Desfazer última partida (Pilha) ----------------
    def desfazer_ultima_partida(self):
        if self.pilha_desfazer.esta_vazia():
            print("\nNão há partidas para desfazer.")
            return

        partida = self.pilha_desfazer.desempilhar()
        self.historico.remover_ultimo()

        jogador1 = partida.jogador1
        jogador2 = partida.jogador2

        # Reverte pontuação
        if partida.resultado == 1:
            jogador1.pontos -= 1
            jogador1.vitorias -= 1
            jogador2.derrotas -= 1
        elif partida.resultado == 2:
            jogador2.pontos -= 1
            jogador2.vitorias -= 1
            jogador1.derrotas -= 1
        else:
            jogador1.pontos -= 0.5
            jogador2.pontos -= 0.5
            jogador1.empates -= 1
            jogador2.empates -= 1

        # Devolve os jogadores para o início da fila de espera
        self._colocar_no_inicio_da_fila(jogador1)
        self._colocar_no_inicio_da_fila(jogador2)

        self.rodada_atual = max(1, self.rodada_atual - 1)
        print(f"\n Partida desfeita: {partida.descricao()}")
        print("   Os jogadores voltaram para o início da fila de espera.")

    def _colocar_no_inicio_da_fila(self, jogador):
        """Recoloca um jogador na frente da fila (usa uma fila auxiliar)."""
        fila_auxiliar = Fila()
        fila_auxiliar.enfileirar(jogador)
        while not self.fila_espera.esta_vazia():
            fila_auxiliar.enfileirar(self.fila_espera.desenfileirar())
        self.fila_espera = fila_auxiliar

    # ---------------- Ranking (usa o Vetor) ----------------
    def ver_ranking(self):
        if self.jogadores.esta_vazio():
            print("\nNenhum jogador cadastrado ainda.")
            return

        lista_ranking = [jogador for jogador in self.jogadores]

        # Ordenação simples (Insertion Sort) por pontos decrescentes,
        # feita manualmente para reforçar o conceito de manipulação do vetor.
        for i in range(1, len(lista_ranking)):
            atual = lista_ranking[i]
            j = i - 1
            while j >= 0 and lista_ranking[j].pontos < atual.pontos:
                lista_ranking[j + 1] = lista_ranking[j]
                j -= 1
            lista_ranking[j + 1] = atual

        print("\n--- Ranking geral do campeonato ---")
        for posicao, jogador in enumerate(lista_ranking, start=1):
            print(f" {posicao}º - {jogador}")


# =============================================================================
# INTERFACE DE LINHA DE COMANDO (CLI)
# =============================================================================
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def exibir_menu():
    print("=" * 60)
    print("       GERENCIADOR DE CAMPEONATO DE XADREZ")
    print("=" * 60)
    print("1 - Cadastrar jogador                 [Vetor]")
    print("2 - Listar jogadores cadastrados       [Vetor]")
    print("3 - Colocar jogador na fila de espera  [Fila]")
    print("4 - Ver fila de espera                 [Fila]")
    print("5 - Registrar resultado de partida     [Fila+Lista+Pilha]")
    print("6 - Ver histórico de partidas          [Lista Encadeada]")
    print("7 - Desfazer última partida            [Pilha]")
    print("8 - Ver ranking geral                  [Vetor]")
    print("0 - Sair")
    print("=" * 60)


def main():
    torneio = TorneioXadrez()

    while True:
        limpar_tela()
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do jogador: ").strip()
            if nome:
                torneio.cadastrar_jogador(nome)
            else:
                print("\n Nome inválido.")
            pausar()

        elif opcao == "2":
            torneio.listar_jogadores()
            pausar()

        elif opcao == "3":
            nome = input("Nome do jogador que entrará na fila: ").strip()
            torneio.entrar_na_fila(nome)
            pausar()

        elif opcao == "4":
            torneio.ver_fila()
            pausar()

        elif opcao == "5":
            torneio.ver_fila()
            if len(torneio.fila_espera) >= 2:
                print("\nResultado da partida:")
                print("1 - Vitória do primeiro jogador da fila")
                print("2 - Vitória do segundo jogador da fila")
                print("0 - Empate")
                resultado = input("Opção: ").strip()
                if resultado in ("0", "1", "2"):
                    torneio.registrar_partida(int(resultado))
                else:
                    print("\n Opção inválida.")
            pausar()

        elif opcao == "6":
            torneio.ver_historico()
            pausar()

        elif opcao == "7":
            torneio.desfazer_ultima_partida()
            pausar()

        elif opcao == "8":
            torneio.ver_ranking()
            pausar()

        elif opcao == "0":
            print("\nEncerrando o Gerenciador de Campeonato de Xadrez. Até logo!")
            time.sleep(1)
            break

        else:
            print("\n Opção inválida, tente novamente.")
            pausar()


if __name__ == "__main__":
    main()
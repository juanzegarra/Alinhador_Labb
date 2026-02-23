## Ainhador LABB

<p align="justify">
Alinhador construído para a mostra de coletivos 2026/01 da Liga de Bioinformática e Biologia Molecular da UFMG. 
A implementação dos algoritmos de Needleman-Wunsch e Smith-Waterman foram baseadas em https://github.com/alevchuk/pairwise-alignment-in-python/tree/master, com modificações. 
A GUI consiste numa primeira tab com duas caixas de texto para digitar as sequências a serem alinhadas, com botões para selecionar o algoritmo de alinhamento (Needleman ou Waterman).

Se clicar em alinhar, uma nova tab é aberta mostrando a matriz de alinhamento colorida no estilo de heatmap (valores maiores com cores quentes, valores menores com cores frias), o caminho realizado pelo alinhador para definir o alinhamento ótimo (traceback) é colorido em verde.
Além disso, à direita da matriz é possível ver o alinhamento em si e seu score. Muito importante citar que os valores de alinhamento (Match = 10, Mismatch = -5, Gap = -5) impactam bastante no score e no alinhamento final.

Antes de rodar, instalar PyQt6:
</p>

```
pip install PyQt6
```

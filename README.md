# Desafio Pratico: Filtro Bayesiano Simplificado em Python

Classificador de e-mails em Python utilizando o conceito de pontuacao probabilistica/pesos para diferenciar e-mails normais (HAM) de mensagens indesejadas (SPAM).

---

## Regras de Negocio

### 1. Base de Conhecimento (Palavras e Pesos)
| Palavra | Peso de Risco de Spam |
| :--- | :---: |
| `pix` | **0.90** |
| `gratis` | **0.80** |
| `urgente` | **0.70** |
| `reuniao` | **0.10** |
| `aula` | **0.05** |

### 2. Regra de Classificacao
- O script analisa o texto do e-mail e identifica as palavras-chave presentes no dicionario.
- Calcula a **Media Aritmetica** dos pesos detectados:
  Média = (Soma dos Pesos das Palavras Detectadas) / (Total de Palavras Detectadas)
- **Criterio de Decisao:**
  - Se Media >= 0.50 -> **SPAM**
  - Se Media < 0.50 -> **E-MAIL NORMAL (HAM)**
  - *Caso de borda:* Se nenhuma palavra for detectada, a media atribuida e `0.00` (evitando divisao por zero).

---

## Como Executar

Execute o arquivo principal pelo terminal:

```bash
python filtro_bayesiano.py
```

---

## Cenarios de Teste Integrados

1. **Teste 1 (SPAM):**
   - Entrada: `"Urgente receba seu pix gratis agora"`
   - Palavras detectadas: `urgente` (0.7), `pix` (0.9), `gratis` (0.8)
   - Media = `(0.7 + 0.9 + 0.8) / 3 = 0.80`
   - Resultado: **SPAM**

2. **Teste 2 (NORMAL / HAM):**
   - Entrada: `"Confirmacao de reuniao para a aula de amanha"`
   - Palavras detectadas: `reuniao` (0.1), `aula` (0.05)
   - Media = `(0.1 + 0.05) / 2 = 0.075`
   - Resultado: **E-MAIL NORMAL (HAM)**

3. **Teste 3 (Caso de borda):**
   - Entrada: `"Ola amigo, tudo bem? Vamos almocar mais tarde?"`
   - Palavras detectadas: nenhuma
   - Media = `0.00`
   - Resultado: **E-MAIL NORMAL (HAM)**
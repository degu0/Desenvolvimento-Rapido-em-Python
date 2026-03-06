# 🧮 Atividade 1 — API Calculadora

API de calculadora desenvolvida como atividade para a aula de **Desenvolvimento Rápido em Python**.

---

## 🛣️ Rotas

### `POST /calculadora`

Recebe dois números e uma operação, retornando o resultado do cálculo.

**Body (JSON):**

| Campo      | Tipo   | Descrição                        |
|------------|--------|----------------------------------|
| `a`        | number | Primeiro número                  |
| `b`        | number | Segundo número                   |
| `operacao` | string | Operação a ser realizada         |

**Resposta:**

```json
"calculadora": {
  "a": 10,
  "b": 5,
  "operacao": "soma",
  "resultado": 15
}
```

---

## 🛠️ Tecnologias

- **Python**
- **Flask**

---

## ▶️ Como rodar

**1. Entre na pasta da atividade:**

```bash
cd .\At_1\
```

**2. Ative o ambiente virtual:**

```bash
.venv\Scripts\activate
```

**3. Execute a API:**

```bash
flask --app api run
```

# JSONPlaceholder Clone

Clone da [JSONPlaceholder](https://jsonplaceholder.typicode.com) feito com Django + Django REST Framework.

## Como rodar

```bash
# Ativar o ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar as migrations
python manage.py migrate

# Popular o banco de dados
python manage.py loaddata initial_data

# Criar superusuário (para acessar o admin)
python manage.py createsuperuser

# Iniciar o servidor
python manage.py runserver
```

A API estará disponível em `http://localhost:8000`.

## Admin

Acesse `http://localhost:8000/admin/` com o superusuário criado para gerenciar os dados pelo painel do Django.

## Documentação

Acesse `http://localhost:8000/api/docs/` para ver a documentação interativa (Swagger UI).

## Recursos disponíveis

| Endpoint | Descrição |
|---|---|
| `/users/` | Usuários |
| `/posts/` | Posts |
| `/comments/` | Comentários |
| `/albums/` | Álbuns |
| `/photos/` | Fotos |
| `/todos/` | Tarefas |

Todos os recursos suportam `GET`, `POST`, `PUT`, `PATCH` e `DELETE`.

### Rotas aninhadas

```
GET /posts/{id}/comments/
GET /users/{id}/posts/
GET /users/{id}/albums/
GET /users/{id}/todos/
GET /albums/{id}/photos/
```

## Descrição e motivação

Projeto simples para demonstrar uma API com controle de acesso, usando a biblioteca Python FastAPI. 
No acesso ao banco de dados foi usada a biblioteca SQLAchemy e, para manter a simplicidade, 
adotamos como banco de dados o [SQlite](https://www.sqlite.org).

A autenticação foi baseada em token JWT, trafegando como um cookie HTTP-Only.


Para obter um mínimo de reatividade no frontend, sem maiores complicações, usamos [HTMX](https://htmx.org). 

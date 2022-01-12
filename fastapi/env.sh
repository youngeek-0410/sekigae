# for containers

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

alias c='clear'

alias dbgenerate='poetry run alembic revision --autogenerate -m'
alias dbupgrade='poetry run alembic upgrade head'
alias dbdowngrade='poetry run alembic downgrade -1'
alias dbhistory='poetry run alembic history --verbose'
alias dbcurrent='poetry run alembic current'

alias runseed='poetry run python app/main.py seed'

alias activate='source /src/.venv/bin/activate'
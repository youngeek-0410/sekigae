# for containers

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

alias c='clear'

alias dbgenerate='cd /src/app/db; poetry run alembic revision --autogenerate -m'
alias dbupgrade='cd /src/app/db; poetry run alembic upgrade head'
alias dbdowngrade='cd /src/app/db; poetry run alembic downgrade -1'
alias dbhistory='cd /src/app/db; poetry run alembic history --verbose'
alias dbcurrent='cd /src/app/db; poetry run alembic current'

alias runseed='cd /src/app; poetry run python main.py seed'

alias activate='source /src/.venv/bin/activate'
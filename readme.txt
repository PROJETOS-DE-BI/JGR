Como Criar e Ativar um Ambiente Virtual
No terminal, navegue até o diretório do seu projeto e execute:

python -m venv venv
.\venv\Scripts\Activate.ps1
Qdo terminar
deactivate

Conclusão
Embora não seja obrigatório, usar um ambiente virtual é uma prática recomendada para garantir um ambiente 
de desenvolvimento limpo e organizado. Se você trabalha com vários projetos Python, a utilização de ambientes 
virtuais pode economizar muito tempo e evitar problemas futuros.

Instale os Pacotes Necessários
python -m pip install pandas plotly streamlit Pillow

Para criar automaticamente um arquivo requirements.txt que inclua os pacotes e suas versões
python -m pip freeze > requirements.txt

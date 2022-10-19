#!/bin/bash

echo "Informe o novo nome do projeto: ";

# entrada de dados em shell
read NEW_NAME;

# lowercase
NEW_NAME="${NEW_NAME,,}"

# lenght string
LEN_NAME=${#NEW_NAME}

# comparação menor que 'less then'
if [ $LEN_NAME -lt 3 ]
then 
    echo "O nome deve conter no minimo 3 letras!"
    # interrompe script
    exit
fi 

echo "renaming project: "$NEW_NAME;

# renomeia pasta na raiz do repositório
mv py-template $NEW_NAME; 

# edicao de conteudo de arquivos com regex
sed -i 's/py-template/'$NEW_NAME'/g' pyproject.toml;

sed -i 's/py-template/'$NEW_NAME'/g' $NEW_NAME/config.py;

sed -i 's/py-template/'$NEW_NAME'/g' $NEW_NAME/settings.toml;

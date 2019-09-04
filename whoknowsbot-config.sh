#!/bin/bash

if [[ `lsb_release -rs` != "18.04" ]]
then
	echo "A versão do UBUNTU deve ser 18.04!.."
else
	echo "Iniciando atualização de pacotes..."
	sudo apt-get update

	echo "Iniciando instalação do Python3.6..."
	sudo apt-get install python3.6

	echo "Iniciando instalação do gerenciador de pacotes pip..."
	sudo apt-get install python3-pip

	echo "Iniciando instalação das dependências do projeto..."
	sudo python3.6 -m pip install python-twitter nltk wordcloud backoff
fi

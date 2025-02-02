#!/bin/bash

# Verifica se o arquivo de log foi passado como argumento
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <caminho_para_o_arquivo_de_log>"
    exit 1
fi

arquivo_log="$1"

# Extrai os IPs únicos do arquivo de log e os exibe
awk -F', ' '{print $2}' "$arquivo_log" | sort | uniq

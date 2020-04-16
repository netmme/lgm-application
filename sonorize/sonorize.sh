#!/bin/bash

# echo "Hello world!"

set -euo pipefail

DIR_SOUNDS="${1}"
readonly DIR_SOUNDS="${DIR_SOUNDS}glm-application/sonorize/sounds"

echo "${DIR_SOUNDS}"

usage() {
    if [ "${1}" == "help" ]; then
        echo "Usage: sonorize <category> <type> | listCategories | listTypes <category>"
        echo "	1. Joue aléatoirement un son pris dans ${DIR_SOUNDS}/<category>/<type>"
        echo "	- <categorie> : Catégorie de sons (human)"
        echo "	- <type> : Type de son (error, warning, ok)"
        echo "	2. Liste les catégories de sons diponibles"
        echo "	3. Liste les types disponibles pour une <category>"

        exit 0
    fi
}


playSound() {
    # On joue ${DIR_SOUNDS}/${1}/${2}/{2}_1.mpr
    # ${1} : catégories du son
    # ${2} : type de son
    echo "${DIR_SOUNDS}/${1}/${2}/${2}_1.mp3"

    ffplay -nodisp -autoexit "${DIR_SOUNDS}/${1}/${2}/${2}_1.mp3" > /dev/null 2>&1

    exit 0
}


listCategories() {
    local directories
    directories="$(ls "${DIR_SOUNDS}")"

    echo "Catégories diponibles :"
    for category in "${directories[@]}"; do
        echo "- ${category}"
    done

    exit 0
}


listTypes() {
    # On affiche la list des types disponibles pour ${1}
    # ${1} : categorie de son
    local directories
    directories="$(ls "${DIR_SOUNDS}"/"${1}")"

    echo "Types disponibles pour la catégories ${1} :"
    for type in "${directories[@]}"; do
        local n
        n="$(find "${DIR_SOUNDS}"/"${1}"/"${type}" -maxdepth 0 | wc -l)"
        echo "- ${type} (${n})"
    done

    exit 0
}

if [ "${#}" == 3 ]; then
    if [ "${2}" == 'listTypes' ]; then
        listTypes "${3}"
    else
        playSound "${2}" "${3}"
    fi
elif [[ "${#}" == 2 && "${2}" == 'listCategories' ]]; then
    listCategories
else
    usage 'help'
fi

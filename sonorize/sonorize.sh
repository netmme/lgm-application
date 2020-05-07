#!/bin/bash

set -euo pipefail

DIR_SOUNDS="${1}"
readonly DIR_SOUNDS="${DIR_SOUNDS}/sonorize/sounds"

# echo "${DIR_SOUNDS}"

usage() {
    if [ "${1}" == "help" ]; then
        echo "Usage: sonorize <path_to_pre-root_dir> <category> <type> | listCategories | listTypes <category>"
        echo "	1. Joue aléatoirement un son pris dans ${DIR_SOUNDS}/<category>/<type>"
        echo "	- <categorie> : Catégorie de sons (human)"
        echo "	- <type> : Type de son (error, warning, ok)"
        echo "	2. Liste les catégories de sons diponibles"
        echo "	3. Liste les types disponibles pour une <category>"
	echo "NB: l'ajout du path est un peu chelou mais c'était nécessaire pour faire des bruits rigolos"
	echo "    avec les git hooks."

        exit 0
    fi
}


playSound() {
    # On joue ${DIR_SOUNDS}/${1}/${2}/{2}_1.mpr
    # ${1} : catégories du son
    # ${2} : type de son
    baseFilename="${2}_"
    nbFiles="$(find "${DIR_SOUNDS}"/"${1}"/"${2}" -maxdepth 1 | wc -l)"
    nbFiles="$(("${nbFiles}" - 1))"
    alea="$(grep -m1 -ao "[1-${nbFiles}]" /dev/urandom | head -n1)"
    filename="${DIR_SOUNDS}/${1}/${2}/${baseFilename}${alea}.mp3"
    # echo "${filename}"

    ffplay -nodisp -autoexit "${filename}" > /dev/null 2>&1

    exit 0
}


listCategories() {
    local directories
    directories="$(find "${DIR_SOUNDS}" -maxdepth 1 -type d | tail -n +2 | sed -e 's/.*sounds\///')"
    readarray -td$'\n' dir_array <<< "${directories}"

    echo "Catégories diponibles :"
    for category in "${dir_array[@]}"; do
        echo "- ${category}"
    done

    exit 0
}


listTypes() {
    # On affiche la list des types disponibles pour ${1}
    # ${1} : categorie de son
    local directories
    directories="$(find "${DIR_SOUNDS}"/"${1}" -maxdepth 1 -type d | tail -n +2 | sed -e 's/.*sounds\/.*\///')"
    readarray -td$'\n' dir_array <<< "${directories}"

    echo "Types disponibles pour la catégories ${1} :"
    for type in "${dir_array[@]}"; do
        local n
        n="$(find "${DIR_SOUNDS}"/"${1}"/"${type}" -maxdepth 1 | wc -l)"
        n="$(("${n}" - 1))"
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

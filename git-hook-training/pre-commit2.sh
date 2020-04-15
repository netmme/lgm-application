#!/bin/bash

echo "It's the captain!"

if git rev-parse --verify HEAD >/dev/null 2>&1
then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=$(git hash-object -t tree /dev/null)
fi

status=0
for file in $(git diff --cached --name-only --diff-filter=A "${against}")
do
    echo ${file}
    if [ $(sed -e '/^ *#/d' -e '/^ *$/d' ${file} | wc -l) -eq 0 ] ; then
        echo "Adding empty scripts to this repository is forbidden: ${file}"
        status=1
    fi
    is_shell=$(file "${file}" | grep shell)
    if [ ${is_shell} == "1" ]; then
        shellcheck "${file}"
        status=$?
    fi
done

exit "${status}"

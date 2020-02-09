#!/bin/bash
if [ -z ${1} ]; then
    echo "Example ${0} 7.4";
else 
    ssh=""
    if [ ${1} == "ssh" ]; then
        first_line=`head -n 1 Dockerfile_php_${1}`
        ssh="ssh"
    else
        first_line=`head -n 1 Dockerfile_php_${1}.x`
    fi
    
    echo ${first_line}
    tmp=(${first_line//:/ })
    tmp=${tmp[2]};
    tmp=(${tmp//-/ })
    arrIN=(${tmp//./ })
    ITER=0
    version=""
    for i in ${arrIN[@]}; do
        #echo ${i}
        version=${version}${i}.
        ITER=$(expr $ITER + 1)
        if [ ${ITER} -eq 2 ]; then
            version="${version%?}"
            echo "Building php ${tmp} using Dockerfile_php_${version}.x file"
            if [ ${1} == "ssh" ]; then
                command="docker build -t deviny/fpm:${tmp}${ssh} ${2} -f Dockerfile_php_ssh ."
            else
                command="docker build -t deviny/fpm:${tmp}${ssh} ${2} -f Dockerfile_php_${version}.x ."
            fi
            echo ${command}
            docker build -t deviny/fpm:${tmp}${ssh} ${2} -f Dockerfile_php_${version}.x .
           exit 
        fi
    done
fi

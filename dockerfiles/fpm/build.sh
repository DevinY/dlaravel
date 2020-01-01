#!/bin/bash
if [ -z ${1} ]; then
    echo "Example ${0} 7.4";
else 
    first_line=`head -n 1 Dockerfile_php_${1}.x`
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
            command="docker build -t devinn/fpm:${tmp} -f Dockerfile_php_${version}.x ."
            echo ${command}
            docker build -t deviny/fpm:${tmp} -f Dockerfile_php_${version}.x .
           exit 
        fi
    done
fi


# run storm on bppy output files

for file in $(find monty_models -name model_[0-9]d\*.pm) ; do
    prop=${file//model_/prop_}
    prop=${prop//.pm/.csl}
    out=${file//model_/res_}
    out=${out//.pm/.txt}

    sed -i "1 s/mdp/dtmc/" $file
    /opt/storm/build/bin/storm --timemem --prism $file --prop $prop > $out
    echo done $file

done



# run storm on bppy output files
# -name model_[0-9]d\*.pm
for file in $(find models -name dice_\*.pm) ; do
    prop=${file//dice_/prop_}
    prop=${prop//.pm/.csl}
    out=${file//dice_/res_}
    out=${out//.pm/.txt}

    sed -i "1 s/mdp/dtmc/" $file
    storm --timemem --prism $file --prop $prop > $out
    #/opt/storm/build/bin/storm --timemem --prism $file --prop $prop > $out
    echo Computation result written to $out

done


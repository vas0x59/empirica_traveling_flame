zerodir=$(pwd)
file=task.txt
for i in $(seq 1 $(wc -l < "$file")); do
    j=$(sed -n "${i}p" "$file")
    echo "Line $i: $j"
    cp  ./xifoam/pp.sh ./xifoam_calcs/$i
    cp  ./xifoam/system/sampleDict ./xifoam_calcs/$i/system
    cd ./xifoam_calcs/$i
    ./pp.sh
    # ./clean.sh && ./prep.sh $j && ./run.sh
    cd $zerodir

done;
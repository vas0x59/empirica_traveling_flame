zerodir=$(pwd)
file=task.txt
for i in $(seq 1 $(wc -l < "$file")); do
    j=$(sed -n "${i}p" "$file")
    echo "Line $i: $j"
    cp -r ./xifoam ./xifoam_calcs/$i
    cd ./xifoam_calcs/$i
    ./clean.sh && ./prep.sh $j && ./run.sh
    cd $zerodir
done


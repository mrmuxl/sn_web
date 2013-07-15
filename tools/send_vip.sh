
for i in `cat f.txt`
do
    echo $i
    curl http://localhost:8000/vipuser/vipuser_test/518279d14e20e/$i
    sleep 2
done

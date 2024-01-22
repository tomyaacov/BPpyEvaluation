# BPjsModelChecking
* measuring time and memory usage of BPjs model checking. Running example:
```shell
/usr/bin/time -lp  mvn clean compile exec:java -Dexec.args="hot_cold 100 1 true"
```
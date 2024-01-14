$delta = 1.0

while ($delta -ge 0.1) {
    $command = ".\venv_pycharm\Scripts\python.exe .\z3_circle_examples.py -n_0 3 -n_m 1000 -d $delta -s"
    Invoke-Expression $command

    $delta -= 0.2
}
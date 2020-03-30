# Optimized Bully Algorithm
Implementation using `Push/Pull model` and `python` for Optimized Bully Algorithm where the node sends election message for higher priorites only.

## Configuration file
  1. The first line is the period time in which if the leader didn't reply, the node assumes that the leader is dead.
  2. The second line is the period time in which if the node didn't receive okay message, it assumes that it's the leader.
  3. The third line is number of machines(n) in the network.
  4. The next n lines is the ip_port for machine and its priority.

## How to run
Run main.py in each machine and give it its ip_port as parameter for example: 
```sh
$ python main.py 127.0.0.1:5555
```

## Team members
[Ayman Azzam](https://github.com/AymanAzzam)

[Menna Fekry](https://github.com/MennaFekry)

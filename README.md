# sv

## Usage

Give the program the executable name and an memory adress of an instruction and it'll create a svg image to visualize
the stack at that moment.

```
./esv.py program 0xffffffff
```

![](fig.png?raw=true)

Dependencies: radare2 and r2pipe for debugging

## TODO

* Add more information to the image (registers, detect pointers types...)
* Parse debugging symbols to give extra information about the variables of the stack
* Make the code beautiful (now it spaguetti-code)

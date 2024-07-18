Writeup
===

## Prologue

Simple tuning web challenge on gather.town. Find the room with a teleporter as the rooms are not connected.

## Walkthrough

In the web console (F12) , type these two commands:

```
gameSpace.maps
gameSpace.teleport(18,18,"Secret")
```

![](./001.PNG)

You may also want to use <https://github.com/michmich112/teleporter> but it is not necessary.

## Eplogue

1. The map cloning does not work, so it create some problem when the chal is released.
2. Found that some contestor don't know how to call the console out.
3. Unintended solution provided by TWY, which can simply string the json to get flag.
4. Contestor mixing up the flags.
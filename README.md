travis-ci-utils
================
[![Build Status](https://travis-ci.org/rindeal/travis-ci-utils.svg?branch=master)](https://travis-ci.org/rindeal/travis-ci-utils)

Python and CLI utilities for your Travis CI jobs

Examples
---------

```python
with Fold("tag.1", desc="My First Proper Travis CI Fold"):
    print("this will be folded")
    with Time():
        print("this will even show timing information in the rightmost column of the travis logviewer")

print(colour("and this will print colourful text", fg="green", bg="red", style="bold+underline"))
```

```shell
$ cmd=travis-ci-utils
$ $cmd fold -start --desc "My First Proper Travis CI Fold" tag.1
$   echo "this will be folded"
$   $cmd time -start timer.1
$     echo "this will even show timing information in the rightmost column of the travis logviewer"
$   $cmd time -end timer.1
$ $cmd fold -end tag.1
```

Utility script for GibbsLDA++(<http://gibbslda.sourceforge.net/>)  
This script calculate P(z|w): probability of topic given word.

### How to use

```
$ ls
calc_pzw.py
model-final.others
model-final.phi
model-final.tassign
model-final.theta
model-final.twords
wordmap.txt

$ python calc_pzw.py > pzw.txt
```
*calc_pzw.py* read *model-final.others*, *model-final.tassign* and *model-final.twords*, and output results to Standard Output.


### Format
Format of output file.

```
word0
    P(z=0|word0)
    P(z=1|word0)
    ...
word1
    P(z=0|word1)
    P(z=1|word1)
    ...
```

For example,

```
bank
    0.45
    0.55
river
    0.8
    0.2
money
    0.26
    0.84
```

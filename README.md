# kraken_to_pagexml

Script that converts [Kraken](https://github.com/mittagessen/kraken) json segmentation output into a PageXML.

## Possible workflow

### Image binarization

Put your scans in a folder and run:

```
for i n *.png
   do kraken -i $i ${i/png/bin.png} binarize
   done
```

### Image segmentation

```
for i in *.bin.png
    do kraken -i $i ${i/bin.png/json} segment -bl
    done
```
 
### Create pagexml

Now run the script:

```
python kraken_to_pagexml.py *.json
```


The PageXML files can further be processed with, for example, [LAREX](https://github.com/OCR4all/LAREX) or [nashi](https://github.com/andbue/nashi)





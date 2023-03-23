# Sample files
---
To execute the test you'll need to have the following files in this folder:

-file-100m.bin (100 megabytes)

-file-500m.bin (500 megabytes)

-file-1G.bim (1 gigabyte)

## Creating the file in POSIX
To creat the files using the dd command, you can use the following commands:

### file-100.bin
```bash
dd if=/dev/random of=file-100m.bin bs=1024 count=$( expr 1024 \* 1 \* 100 )
```
### file-500m.bin
```bash
dd if=/dev/random of=file-500m.bin bs=1024 count=$( expr 1024 \* 1 \* 500 )
```
### file-1g.binq
```bash
dd if=/dev/random of=file-1024m.bin bs=1024 count=$( expr 1024 \* 1024 \* 1 )
```


# hexprint - hex-dump tool
This is a simple hex-dump utility, with an output format very similar to the old DEBUG.EXE program that shipped with MS-DOS. It takes three parameters on the command line:

* 1st parameter = filename
* 2nd parameter = offset from start of file
* 3rd parameter = number of bytes to print

The output format looks like this:
```
---------------------------------------------------------------------------
filename.txt
---------------------------------------------------------------------------
00000000  00 00 00 00 00 00 00 00-41 42 43 44 45 46 47 48  ........ABCDEFGH
00000010  61 62 63 64 65 66 67 68-FF FF FF FF FF FF FF FF  abcdefgh........
```
Only simple ASCII characters are displayed in the column to the right. All other characters are displayed as a period (.).


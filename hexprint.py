"""Hex dump utility, with output format similar to DOS debug.

1st command-line argument = filename
2nd command-line argument = offset (of first byte to display)
3rd command-line argument = total # bytes to display (0=all)
"""
import binascii
import sys

#------------------------------------------------------------------------------
def hexdump(filename=None, offset=0, totbytes=0):
    """Hex dump utility, with output format similar to DOS debug.

    filename = filename
    offset = offset (of first byte to display)
    totbytes = total # bytes to display (0=all)
    """
    bytes_printed = 0

    f = open(filename,'rb')
    f.seek(offset)
    row_offset = 16 * (offset//16) # the file offset for first byte in current row
    row_string = '' # the displayed string version of this row (printed on the right)
    row_values = 0 # number of hex values printed so far on current row

    print('-'*75)
    print(filename)
    print('-'*75)

    if offset % 16 != 0:
        # not starting at the beginning of a row
        print(format("%0.8X" % row_offset) + '  ', end="")
        row_string = ''
        for i in range(0,offset % 16):
            row_string += ' '
            print(' '*3, end="")
            row_values += 1

    while True:

        if f.tell() % 16 == 0:
            print(format("%0.8X" % row_offset) + '  ', end="")
            row_values = 0

        nextbyte = f.read(1)
        if len(nextbyte) != 1:
            break

        print( format("%0.2X" % ord(nextbyte)), end="")
        print( '-' if f.tell() % 16 == 8 else ' ', end="" )
        if ord(nextbyte) in range(32,128):
            row_string += nextbyte.decode(encoding='UTF-8')
        else:
            row_string += '.'

        if f.tell() % 16 == 0:
            print(' ' + row_string)
            row_offset += 16
            row_string = ''
            row_values = 0

        bytes_printed += 1
        row_values += 1
        if totbytes > 0 and bytes_printed == totbytes:
            break

    # if the final row is a partial (contains less than 16 values), then
    # need to print blanks for missing hex values and then print row_string
    if row_values < 16:
        print('   '*(16-row_values) + ' ' + row_string)

    f.close()
    return bytes_printed

#------------------------------------------------------------------------------
if __name__ == "__main__":
    hexdump(filename='readme.md', offset=10, totbytes=100)

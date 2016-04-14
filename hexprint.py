"""Hex dump utility, with output format similar to DOS debug.

cli() -----------> Handle command-line arguments.
hexdump() -------> Display hex dump to the console.
"""
import os
import sys

import click

#------------------------------------------------------------------------------
def cli():
    """Command-line wrapper for hexdump() function.

    Handles these command-line arguments:
    1st argument = filename
    2nd argument = offset of first byte to display (default = 0)
    3rd argument = # bytes to display (default = 0 = entire file)

    Displays a hex dump of the specified portion of the specified file.
    """

    # note that sys.argv[0] is the name of the script, so we start at argv[1]
    if len(sys.argv) < 2:
        click.echo('Syntax --> hexprint filename offset nbytes (offset/nbytes are optional)')
        return

    filename = sys.argv[1]
    offset = 0 if len(sys.argv) < 3 else int(sys.argv[2])
    totbytes = 0 if len(sys.argv) < 4 else int(sys.argv[3])
    hexdump(filename=filename, offset=offset, totbytes=totbytes)

#------------------------------------------------------------------------------
def hexdump(filename=None, offset=0, totbytes=0):
    """Hex dump utility, with output format similar to DOS debug.

    filename = filename
    offset = offset (of first byte to display); if negative, offset is from EOF
    totbytes = total # bytes to display (0=all)
    """
    bytes_printed = 0

    file_size = os.stat(filename).st_size
    fhandle = open(filename, 'rb')
    if offset < 0:
        # negative offset is from end of file
        fhandle.seek(offset, 2)
        # file_position = the true offset of starting byte (from beginning of file)
        file_position = file_size + offset
        row_offset = 16 * (file_position//16) # offset to first byte in current row
    else:
        # positive offset is from beginning of file
        fhandle.seek(offset)
        row_offset = 16 * (offset//16) # offset to first byte in current row

    row_string = '' # the displayed string version of this row (printed on the right)
    row_values = 0 # number of hex values printed so far on current row

    click.echo('-'*75)
    click.echo(click.style(filename, fg='green'))
    click.echo(11*'-' + '0--1--2--3--4--5--6--7--8--9--A--B--C--D--E--F' + 18*'-')

    if offset % 16 != 0:
        # not starting at the beginning of a row
        click.echo(format("%0.8X" % row_offset) + '  ', nl=False)
        row_string = ''
        for _ in range(offset % 16):
            row_string += ' '
            click.echo(' '*3, nl=False)
            row_values += 1

    while True:

        if fhandle.tell() % 16 == 0:
            click.echo(format("%0.8X" % row_offset) + '  ', nl=False)
            row_values = 0

        nextbyte = fhandle.read(1)
        if len(nextbyte) != 1:
            break

        click.echo(format("%0.2X" % ord(nextbyte)), nl=False)
        click.echo('-' if fhandle.tell() % 16 == 8 else ' ', nl=False)
        if ord(nextbyte) in range(32, 128):
            row_string += nextbyte.decode(encoding='UTF-8')
        else:
            row_string += '.'

        if fhandle.tell() % 16 == 0:
            click.echo(click.style(' ' + row_string, fg='green'))
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
        click.echo('   '*(16-row_values) + ' ', nl=False)
        click.echo(click.style(row_string, fg='green'))

    fhandle.close()
    return bytes_printed

#------------------------------------------------------------------------------
if __name__ == "__main__":
    cli()

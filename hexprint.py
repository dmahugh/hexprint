"""Hex dump utility, with output format similar to DOS debug.

cli() ------------> Handle command-line arguments.
hexdump() --------> Display hex dump to the console.
test_cli_help() --> Test the --help option.
"""
import os
import tempfile

import click
from click.testing import CliRunner

#------------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS, options_metavar='<options>')
@click.argument('file', type=click.Path(exists=True), metavar="file")
@click.option('-n', '--nbytes', default=0,
              help='# bytes to display. ' +
              'default = 0 (entire file)', metavar='<int>')
@click.option('-o', '--offset', default=0,
              help='Offset of first byte (default=0). ' +
              'Negative values are relative to end of file.',
              metavar='<int>')
@click.version_option(version='1.0', prog_name='Hexprint')
def cli(file, offset, nbytes):
    """\b
    ---------------
     | ? | ? | ? |      file = file to read and display
    ---------------
     | ? | ? | ? |      Prints hex dump of file contents.
    ---------------
    """
    hexdump(filename=file, offset=offset, totbytes=nbytes)

#------------------------------------------------------------------------------
def hexdump(*, filename=None, offset=0, totbytes=0):
    """Hex dump utility, with output format similar to DOS debug.

    filename = filename
    offset = offset (of first byte to display); if negative, offset is from EOF
    totbytes = total # bytes to display (0=all)
    """
    bytes_printed = 0

    try:
        fhandle = open(filename, 'rb')
    except PermissionError:
        click.echo(click.style('Can not open file: ' + click.format_filename(filename), fg='red'))
        return

    if offset < 0:
        # negative offset is from end of file
        fhandle.seek(offset, 2)
        file_size = os.stat(filename).st_size
        true_offset = file_size + offset # offset from beginning of file
    else:
        # positive offset is from beginning of file
        fhandle.seek(offset)
        true_offset = offset

    row_string = '' # the displayed string version of this row (printed on the right)
    row_values = 0 # number of hex values printed so far on current row
    row_offset = 16 * (true_offset//16) # offset to first byte in current row

    click.echo(click.style('-'*75, fg='blue'))
    click.echo(filename)
    click.echo(click.style(9*'-', fg='blue'), nl=False)
    for col_offset in range(16):
        click.echo(click.style('--', fg='blue'), nl=False)
        click.echo(click.style(hex(col_offset)[2].upper(), fg='cyan'), nl=False)
    click.echo(click.style(18*'-', fg='blue'))

    if true_offset % 16 != 0:
        # not starting at the beginning of a row
        click.echo(click.style(format("%0.8X" % row_offset) + '  ', fg='cyan'), nl=False)
        row_string = ''
        for _ in range(true_offset % 16):
            row_string += ' '
            click.echo(' '*3, nl=False)
            row_values += 1

    while True:

        if fhandle.tell() % 16 == 0:
            click.echo(click.style(format("%0.8X" % row_offset) + '  ', fg='cyan'), nl=False)
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
            click.echo(' ' + row_string)
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
        click.echo(row_string)

    fhandle.close()
    return bytes_printed

#------------------------------------------------------------------------------
def test_cli_help():
    """Test the --help option.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert result.output.startswith('Usage: cli <options> file\n')

#------------------------------------------------------------------------------
def test_cli_values():
    """Test reading values from a tempfile with known contents.
    """
    tempfilename = next(tempfile._get_candidate_names()) + '.tmp'
    with open(tempfilename, 'w') as fhandle:
        fhandle.write('This is a test.') # write temporary test file

    runner = CliRunner()
    result = runner.invoke(cli, [tempfilename])
    assert result.exit_code == 0

    # get the first (and only) line of hex data in the output
    outputdata = result.output.split('\n')[3]
    assert outputdata == \
        '00000000  54 68 69 73 20 69 73 20-61 20 74 65 73 74 2E     This is a test.'

    os.remove(tempfilename) # delete the temporary test file

# code to execute when running standalone: -------------------------------------
if __name__ == '__main__':
    test_cli_values()

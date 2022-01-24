"""
Inspired by `zxpy`(https://github.com/tusharsadhwani/zxpy), but no need to use `zxpy` to launch anymore
"""
import codecs
import contextlib
import os
import subprocess
from typing import Generator, Tuple, IO

UTF8Decoder = codecs.getincrementaldecoder("utf8")


@contextlib.contextmanager
def create_shell_process(command: str) -> Generator[IO[bytes], None, None]:
    """Creates a shell process, yielding its stdout to read data from."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    assert process.stdout is not None
    yield process.stdout

    process.wait()
    process.stdout.close()
    if process.returncode != 0:
        raise ChildProcessError(process.returncode)


def sh(command: str) -> Tuple[str, int]:
    """
    Launch shell command
    :param command: shell command in string
    :return: stdout + stderr, return code
    """
    stdout_buffer = ''
    ret_code = 0
    try:
        with create_shell_process(command) as stdout:
            decoder = UTF8Decoder()
            with open(stdout.fileno(), 'rb', closefd=False) as buff:
                for text in iter(buff.read1, b""):  # type: ignore
                    text = decoder.decode(text)
                    stdout_buffer += text
                    print(text, end='')
                decoder.decode(b'', final=True)
    except ChildProcessError as e:
        ret_code = e
    return stdout_buffer, ret_code


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


if __name__ == '__main__':
    out, code = sh('ls -l')
    print(out)
    print(code)

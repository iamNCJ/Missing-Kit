"""
Inspired by `zxpy`(https://github.com/tusharsadhwani/zxpy), but no need to use `zxpy` to launch anymore
"""

import subprocess
from typing import Tuple


def sh(command: str) -> Tuple[str, str, int]:
    """
    Launch shell command
    :param command: shell command in string
    :return: stdout, stderr, return code
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    stdout_text, stderr_text = process.communicate()
    assert process.stdout is not None
    assert process.stderr is not None
    assert process.returncode is not None

    return (
        stdout_text.decode(),
        stderr_text.decode(),
        process.returncode,
    )


if __name__ == '__main__':
    std, err, ret = sh('ls .')
    print(f'std: {std}')
    print(f'err: {err}')
    print(f'ret: {ret}')

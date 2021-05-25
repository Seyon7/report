from click.testing import CliRunner
from modules.report6 import *


def test_driver():
    runner = CliRunner()
    result = runner.invoke(cli_root, ["-f", "../data", "driver", "Sebastian Vettel"])
    assert result.exit_code == 0
    assert "Sebastian Vettel              | FERRARI                            | 0:01:04.415" in result.output


def test_ls():
    runner = CliRunner()
    result = runner.invoke(cli_root, ["--files", "../data", "ls"])
    assert result.exit_code == 0
    assert result.output.startswith("  1. Augusto Pinochet              | VAZ 2101                           | 0:01:00.001")

    result = runner.invoke(cli_root, ["-f", "../data", "ls", "asc"])
    assert result.exit_code == 0
    assert result.output.startswith("  1. Augusto Pinochet              | VAZ 2101                           | 0:01:00.001")

    result = runner.invoke(cli_root, ["-f", "../data", "ls", "desc"])
    assert result.exit_code == 0
    assert result.output.startswith(" 16. Kevin Magnussen               | HAAS FERRARI                       | 0:01:13.393")

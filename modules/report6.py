import click
from modules.processor import build_report, print_report


@click.group(invoke_without_command=True)
@click.option('--files', '-f', required=True, type=str, prompt="Provide the path to data files")
@click.pass_context
def cli_root(ctx, files):
    ctx.meta['files'] = files


@cli_root.command()
@click.argument('name', type=str)
@click.pass_context
def driver(ctx, name):
    files = ctx.meta['files']
    report = build_report(files, driver=name)
    print_report(report)


@cli_root.command()
@click.argument('order', type=click.Choice(["asc", "desc"]), default="asc")
@click.pass_context
def ls(ctx, order):
    files = ctx.meta['files']
    if order not in ("asc", "desc"):
        raise IOError("'Wrong sorting direction")
    report = build_report(files, order=order)
    # добавить логинку того, что если нет error_log, то это это ошибка. подумать, куда добавть эту проверку
    print_report(report)

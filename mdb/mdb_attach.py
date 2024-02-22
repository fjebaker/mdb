# Copyright 2023-2024 Tom Meltzer. See the top-level COPYRIGHT file for
# details.

import asyncio
import functools
import logging
import signal

import click
from typing_extensions import TypedDict

from .mdb_client import Client
from .mdb_shell import mdbShell

ShellOpts = TypedDict(
    "ShellOpts",
    {
        "ranks": int,
        "select": str,
        "host": str,
        "port": int,
        "breakpt": str,
        "exec_script": str,
        "plot_lib": str,
    },
)


@click.command()
@click.option(
    "-h",
    "--hostname",
    default="localhost",
    show_default=True,
    help="Hostname where exchange server is running.",
)
@click.option(
    "-p",
    "--port",
    default=2000,
    show_default=True,
    help="Starting port address. Each rank's port is assigned as [port_address + rank].",
)
@click.option(
    "-s",
    "--select",
    default=None,
    show_default=True,
    help="Rank(s) to debug e.g., 0,3-5 will debug ranks 0,3,4 and 5. If empty all ranks will be selected. Note ranks starts with zero index.",
)
@click.option(
    "-x",
    "--exec-script",
    type=click.File("r"),
    help="Execute a set of mdb commands contained in a script file.",
)
@click.option(
    "--plot-lib",
    default="termgraph",
    show_default=True,
    help="Plotting library to use. Recommended default is [termgraph] but if this is not available [matplotlib] will be used. [matplotlib] is best if there are many ranks to debug e.g., -n 100.",
)
def attach(
    hostname: str,
    port: int,
    select: str,
    exec_script: click.File,
    plot_lib: str,
) -> None:
    """Attach to mdb debug server.

    Example:

    $ mdb attach -x script.mdb
    """

    logging.basicConfig(
        filename="mdb-attach.log", encoding="utf-8", level=logging.DEBUG
    )

    supported_plot_libs = ["termgraph", "matplotlib"]
    if plot_lib not in supported_plot_libs:
        msg = f"warning: unrecognized plot library [{plot_lib}]. Supported libraries are [{supported_plot_libs}]."
        raise ValueError(msg)

    if exec_script is None:
        script = None
    else:
        script = exec_script.name

    client_opts = {
        "exchange_hostname": hostname,
        "exchange_port": port,
    }
    client = Client(opts=client_opts)

    loop = asyncio.get_event_loop()

    try:
        # loop = asyncio.get_event_loop()
        loop.run_until_complete(client.connect())
    except ConnectionError as e:
        print(e)
        exit(1)

    ranks = client.number_of_ranks

    # debug all ranks if "select" is not set
    if select is None:
        select = f"0-{ranks - 1}"

    shell_opts: ShellOpts = {
        "select": select,
        "ranks": ranks,
        "exec_script": script,
        "plot_lib": plot_lib,
        "backend": client.backend,
    }

    # def interrupt(args):
    #     print("args = \n", args)
    #     getattr(signal, signame),
    #     functools.partial(ask_exit, signame, loop))

    def ask_exit(signame, loop):
        print("got signal %s: exit" % signame)
        # print("asyncio.all_tasks(loop) = \n", asyncio.all_tasks(loop))
        interruptclient = Client(opts=client_opts)
        loop.create_task(interruptclient.connect())
        # loop.create_task(interruptclient.run_command("interrupt"))
        loop.create_task(interruptclient.run_command("interrupt"))
        # asyncio.create_task(interruptclient.run_command("interrupt"))

    mshell = mdbShell(shell_opts, client)

    # loop.add_signal_handler(signal.SIGINT, interrupt, "something")
    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(
            getattr(signal, signame), functools.partial(ask_exit, signame, loop)
        )

    mshell.cmdloop()
    loop.close()

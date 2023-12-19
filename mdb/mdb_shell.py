import cmd
import itertools
import re
import sys

import matplotlib.pyplot as plt
import numpy as np

from .utils import parse_ranks

GDBPROMPT = r"\(gdb\)"
plt.style.use("dark_background")


class mdbShell(cmd.Cmd):
    intro = "mdb - mpi debugger - built on gdb. Type ? for more info"
    prompt = "(mdb) "
    select = list()
    ranks = list()
    client = None

    def __init__(self, prog_opts, client):
        self.ranks = prog_opts["ranks"]
        select_str = prog_opts["select"]
        self.select = parse_ranks(select_str)
        self.prompt = f"(mdb {select_str}) "
        self.client = client
        super().__init__()

    def do_interact(self, rank):
        """
        Description:
        Jump into interactive mode for a specific rank.

        Example:
        The following command will debug the 2nd process (proc id 1)

            (mdb) interact 1
        """
        rank = int(rank)
        if rank not in self.select:
            print(f"rank {rank} is not one of the selected ranks {self.select}")
            return
        c = self.client.dbg_procs[rank]
        sys.stdout.write("\r(gdb) ")
        c.interact()
        sys.stdout.write("\r")
        return

    def do_print(self, var):
        """
        Description:
        Print [var] on every selected process.

        Example:
        The following command will print variable [var] on all selected processes.

            (mdb) pprint [var]
        """

        def send_print(var, rank):
            c = self.client.dbg_procs[rank]
            c.sendline(f"print {var}")
            c.expect(GDBPROMPT)
            output = c.before.decode("utf-8")
            result = 0.0
            for line in output.split("\n"):
                float_regex = r"\d+ = ([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)"
                m = re.search(float_regex, line)
                if m:
                    result = m.group(1)
                    try:
                        result = float(result)
                    except ValueError:
                        print(f"cannot convert variable [{var}] to a float.")
                        return
            return rank, result

        ranks = []
        results = []
        for rank, result in self.client.pool.starmap(
            send_print, zip(itertools.repeat(var), self.select)
        ):
            ranks.append(str(rank))  # string for barchart labels
            results.append(result)

        results = np.array(results)
        print(
            f"min : {results.min()}\nmax : {results.max()}\nmean: {results.mean()}\nn    : {len(results)}"
        )

        fig, ax = plt.subplots()
        ax.bar(ranks, results)
        ax.set_xlabel("rank")
        ax.set_ylabel("value")
        ax.set_title(var)
        plt.show()

        return

    def do_clearbuffers(self, args):
        """
        Description:
        Clear all process stdout buffers.

        Example:
        The following command will clear the stdout buffer for each process.

            (mdb) clearbuffers
        """
        for rank in range(self.ranks):
            c = self.client.dbg_procs[rank]
            while True:
                if c.before:
                    c.expect(r".+")
                else:
                    break
        print("cleared")

    def do_command(self, command):
        """
        Description:
        Run [command] on every process.

        Example:
        The following command will run gdb command [command] on every process.

            (mdb) pcommand [command]
        """

        def send_command(command, rank):
            c = self.client.dbg_procs[rank]
            c.sendline(command)
            c.expect(GDBPROMPT)
            print(f"{rank}: " + c.before.decode("utf-8"), end="\n")
            return

        self.client.pool.starmap(
            send_command, zip(itertools.repeat(command), self.select)
        )

        return
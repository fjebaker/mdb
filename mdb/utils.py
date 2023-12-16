import re

def parse_ranks(ranks):

    ranks = re.sub(
            r'(\d+)-(\d+)',
            lambda match: ','.join(str(i) for i in range(int(match.group(1)), int(match.group(2)) + 1)
                ),
            ranks
            )
    ranks = set([int(s) for s in ranks.split(',')])

    return ranks

import re
from gensim.parsing.preprocessing import preprocess_string

REL_THRESHOLD = 0.5


def relevance_filter(tags, resume):
    if not tags:
        return False

    tags = list(map(lambda x: preprocess_string(str(x))[0], tags))
    resume = " ".join(preprocess_string(resume))

    n_mach = sum([len(re.findall(f"\\b{tag}\\b", resume)) for tag in tags])
    return n_mach / len(tags) > REL_THRESHOLD
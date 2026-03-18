import os
from .template import Settings
from .fushionizer import Fusionizer


def main(
        fq1: str,
        fq2: str,
        star_index_dir: str,
        assembly_fa: str,
        annotation_gtf: str,
        blacklist_tsv: str,
        known_fusions_tsv: str,
        protein_domains_gff3: str,
        cytobands_tsv: str,
        outdir: str,
        threads: int,
        debug: bool,
    ):

    prefix = os.path.basename(outdir)
    for c in [' ', ',', '(', ')']:
        prefix = prefix.replace(c, '_')
    workdir = get_temp_path(prefix=f'./{prefix}_')

    settings = Settings(
        workdir=workdir,
        outdir=outdir,
        threads=threads,
        debug=debug,
        mock=False)

    Fusionizer(settings=settings).main(
        fq1=fq1,
        fq2=fq2,
        star_index_dir=star_index_dir,
        assembly_fa=assembly_fa,
        annotation_gtf=annotation_gtf,
        blacklist_tsv=None if blacklist_tsv.lower() == 'none' else blacklist_tsv,
        known_fusions_tsv=None if known_fusions_tsv.lower() == 'none' else known_fusions_tsv,
        protein_domains_gff3=None if protein_domains_gff3.lower() == 'none' else protein_domains_gff3,
        cytobands_tsv=None if cytobands_tsv.lower() == 'none' else cytobands_tsv,
    )


def get_temp_path(
        prefix: str = 'temp',
        suffix: str = '') -> str:

    i = 1
    while True:
        fpath = f'{prefix}{i:03}{suffix}'
        if not os.path.exists(fpath):
            return fpath
        i += 1

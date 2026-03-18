import argparse
import fusionizer


__VERSION__ = '1.0.0'


PROG = 'python fusionizer'
DESCRIPTION = f'RNA-seq fusion detection pipeline (version {__VERSION__}) by Yu-Cheng Lin (ylin@nycu.edu.tw)'
REQUIRED = [
    {
        'keys': ['-1', '--fq1'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to read 1 FASTQ (.fastq.gz) file',
        }
    },
    {
        'keys': ['-2', '--fq2'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to read 2 FASTQ (.fastq.gz) file',
        }
    },
    {
        'keys': ['-i', '--star-index-dir'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to STAR genome index directory',
        }
    },
    {
        'keys': ['-a', '--assembly-fa'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to genome assembly FASTA (.fa) file',
        }
    },
    {
        'keys': ['-g', '--annotation-gtf'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to gene annotation GTF (.gtf) file',
        }
    },
]
OPTIONAL = [
    {
        'keys': ['--blacklist-tsv'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'None',
            'help': 'path to Arriba blacklist TSV file (default: %(default)s)',
        }
    },
    {
        'keys': ['--known-fusions-tsv'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'None',
            'help': 'path to Arriba known fusions TSV file (default: %(default)s)',
        }
    },
    {
        'keys': ['--protein-domains-gff3'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'None',
            'help': 'path to Arriba protein domains GFF3 file (default: %(default)s)',
        }
    },
    {
        'keys': ['--cytobands-tsv'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'None',
            'help': 'path to Arriba cytobands TSV file (default: %(default)s)',
        }
    },
    {
        'keys': ['-o', '--outdir'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'fusionizer_output',
            'help': 'path to the output directory (default: %(default)s)',
        }
    },
    {
        'keys': ['-t', '--threads'],
        'properties': {
            'type': int,
            'required': False,
            'default': 4,
            'help': 'number of CPU threads (default: %(default)s)',
        }
    },
    {
        'keys': ['-d', '--debug'],
        'properties': {
            'action': 'store_true',
            'help': 'debug mode',
        }
    },
    {
        'keys': ['-h', '--help'],
        'properties': {
            'action': 'help',
            'help': 'show this help message',
        }
    },
    {
        'keys': ['-v', '--version'],
        'properties': {
            'action': 'version',
            'version': __VERSION__,
            'help': 'show version',
        }
    },
]


class EntryPoint:

    parser: argparse.ArgumentParser

    def main(self):
        self.set_parser()
        self.add_required_arguments()
        self.add_optional_arguments()
        self.run()

    def set_parser(self):
        self.parser = argparse.ArgumentParser(
            prog=PROG,
            description=DESCRIPTION,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter)

    def add_required_arguments(self):
        group = self.parser.add_argument_group('Required')
        for item in REQUIRED:
            group.add_argument(*item['keys'], **item['properties'])

    def add_optional_arguments(self):
        group = self.parser.add_argument_group('Optional')
        for item in OPTIONAL:
            group.add_argument(*item['keys'], **item['properties'])

    def run(self):
        args = self.parser.parse_args()
        print(f'Start running Fusionizer version {__VERSION__}\n', flush=True)
        fusionizer.main(
            fq1=args.fq1,
            fq2=args.fq2,
            star_index_dir=args.star_index_dir,
            assembly_fa=args.assembly_fa,
            annotation_gtf=args.annotation_gtf,
            blacklist_tsv=args.blacklist_tsv,
            known_fusions_tsv=args.known_fusions_tsv,
            protein_domains_gff3=args.protein_domains_gff3,
            cytobands_tsv=args.cytobands_tsv,
            outdir=args.outdir,
            threads=args.threads,
            debug=args.debug)


if __name__ == '__main__':
    EntryPoint().main()

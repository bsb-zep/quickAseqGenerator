import quickAseqGenerator
import sys


# run from repo root:
# python cli-aseqFromCache.py BV013301038 n DHB test2
# python cli-aseqFromCache.py [BV id] [n or q] [string] [jobname]

quickAseqGenerator.tools.aseqFromCache(sys.argv)

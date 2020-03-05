# cache-based ASEQ generator

This tool uses caching to provide an on-demand generator for ASEQ enrichment instructions. It requires access to the public B3Kat APIs only.

## Setup

### System requirements
Python 3.x and the third-party libraries lxml and requests are required. They are available through ``pip`` and should use the most current version available for your local Pyhon installation.

Because the ASEQ generator is controlled through text files (for BV ID lists) and on command line, it is recommended to use a IDE with terminal integration (like Visual Studio Code).

### Installation

If you have both Python 3.x and 2.x installed locally (which is still default in some linux distributions as well as in MacOS), please use ``pip3`` instead of ``pip``.

    pip install lxml
    pip install requests
    git clone [this repository]
    cd [repository folder]
    mkdir bvCache
    mkdir jobs
    touch cache.log
    touch error.log

After you have succesfully completed this process, you can use the workflow as described below.

## Workflow

1. Generate Cache
   - Collect all BV IDs for processing in a list file, using plain text and one BV ID per line.
   - Apply tool-B3KatToCache.py as described below. If you wisch to delete the list file after processing, use the ``dodel`` switch at the end of the command line, otherwise set ``nodel`` to keep the list file untouched.

            python tool-B3KatToCache.py [bvId list file] [nodel/dodel]

    - Do not delete the queue-processed.bvid file, because you will need it for updating the cache later!!
    - If there are any BV IDs in the queue-rescheduled.bvid file, this means that there were errors while querying the B3Kat public APIs while processing them. You should try processing this queue file again some hours later:

            python tool-B3KatToCache.py queue-rescheduled.bvid dodel
    
    If they still fail, check the B3Kat portal at gateway-bayern.de (or if you have, use your ALEPH client account) whether the dataset still exists. Due to the way B3Kat handles deletions, deleted B3Kat entries will appear as errors in this tool.

2. Update Cache (if necessary)
    - If the cache has not been generated very recently, you might like to update the cache. To do this, run the updater tool on queue-processed.bvid:

            python tool-B3KatToCache.py queue-processed.bvid nodel

    - Again, if there are any errors, consider to rerun the rescheduled queue:

            python tool-B3KatToCache.py queue-rescheduled.bvid dodel
    
3. Generate a list of dataset enrichment ASEQ lines
    - Collect all BV IDs that you whish to enrich with a ``ASEQ 078n`` or ``ASEQ 078q`` field in a list file, using plain text and one BV ID per line. All BV IDs must have been cached before.
    - Apply cli-batchAseqFromCache.py as described below. As this operation uses the cached state of the B3Kat datasets, you will not need an internet connection for this.
     
            python tool-batchAseqFromCache.py [input filename] [n/q] [new field value] [job description]
        
        This means: All BV IDs from the file specified by ``[input filename]`` will receive a 078 ``[n/q]`` field with the string contents ``[new field value]``. Any log lines and the resulting ASEQ file name will contain the ``[[job description]``.

    - From the log file, you will be able to see which datasets did already contain an exactly corresponding 078 n/q field, which caused them to be omitted from duplicate enrichment.

    - The log will also list all BV IDs that were not in cache. They have to be saved into the cache (step 1), before an ASEQ line can be generated for them.

# cache-based ASEQ generator

This tool uses caching to provide an on-demand generator for ASEQ enrichment instructions. It requires access to the public B3Kat APIs to build and update a local data cache. All ASEQ writing tools can be run from the cache and do not require realtime internet connection.


## Setup

### System requirements
* Python 3.8.x with `pip` and `venv` modules installed
* to comfortably read and search through the aseq files, an IDE or `grep` is recommended

### Installation

If you have both Python 3.x and 2.x installed, please use `python3` instead of `python` and `pip3` instead of `pip`. 

    git clone [this repository]
    cd [repository folder]
    python -m venv venv
    # use this for linux/bash prompts, for windows specified below
    source venv/bin/activate
    # use this for windows prompts, for linux/bash specified above
    venv/Scripts/activate
    mkdir bvCache
    mkdir jobs
    touch cache.log
    touch error.log


## Workflow

1. Generate Cache
   - Collect all BV IDs for processing in a list file, using plain text and one BV ID per line.
   - Apply tool-B3KatToCache.py as described below. If you wisch to delete the list file after processing, use the ``dodel`` switch at the end of the command line, otherwise set ``nodel`` to keep the list file untouched.
   - To speed up the process, you can configure the tool to run several queries simultaneously. The helpfulness of this option will depend on the B3Kat server resources and on your internet connection. Do not overload the B3Kat servers!

            python tool-B3KatToCache.py [bvId list file] [nodel/dodel] [optional: number of simultaneous jobs]
            python tool-B3KatToCache.py listfile.txt nodel 2

    - Do not delete the queue-processed.bvid file, because you will need it for updating the cache later!!
    - If there are any BV IDs in the queue-rescheduled.bvid file, this means that there were errors while querying the B3Kat public APIs while processing them. You should try processing this queue file again some hours later:

            python tool-B3KatToCache.py queue-rescheduled.bvid dodel
    
    If they still fail, check the B3Kat portal at gateway-bayern.de (or if you have, use your ALEPH client account) whether the dataset still exists. Due to the way B3Kat handles deletions, deleted B3Kat entries will appear as errors in this tool. Currently the only way to remove deleted datasets from the local cache is to rebuild it from scratch, meaning you have to remove all files from the `bvCache` directory and run the command described below for "Update Cache".

2. Update Cache
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

4. Prepare an ASEQ file for import queue
    - To feed an ASEQ file into the ALEPH import queue, all lines should be grouped by sysId. The sorting tool also provides a sysId counter to limit the number of datasets changed. This is helpful for files with multiple ASEQ rows per dataset.

            python tool-sortFile.py [file name] [optional: maximum number of datasets changed]

      The resulting file `[file name].sorted2` will only contain the ASEQ lines within this limit. If the maximum number of datasets changed is reached, the processing will stop. The input file will not be changed.
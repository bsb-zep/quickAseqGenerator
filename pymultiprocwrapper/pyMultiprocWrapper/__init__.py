import multiprocessing
from tqdm import tqdm

class pyMultiprocWrapper(object):

    # the step function to be wrapped
    stepFunction = object()

    # queue as input parameter for stepFunction
    queue = list()

    # number of parallel jobs, default is 2
    parallelLimit = 2

    # subqueued elements
    subqueuedQueue = list()

    # register a function as step function
    def registerFunction(self, stepFunction):
        if callable(stepFunction):
            self.stepFunction = stepFunction
        else:
            raise ImportError('illegal type for stepFunction: '+ str(type(stepFunction)))
        return True
    
    def registerQueue(self, queueObject):
        # check whether queueObject is of allowed type
        if (isinstance(queueObject, list) or
            isinstance(queueObject, tuple) or
            isinstance(queueObject, set)) and (len(queueObject) != 0):
            # if allowed type, schedule queue
            self.queue = queueObject
        else:
            raise TypeError('expected list, tuple or set as queue but received ' + 
                            str(type(queueObject)))
        return True
    
    # set limit for parallel jobs and adjust subqueues accordingly
    def setParallelLimit(self, parallelLimit):
        if isinstance(parallelLimit, int):
            self.parallelLimit = parallelLimit
        else:
            raise TypeError('illegal type for parallel jobs limit')
        if len(self.subqueuedQueue) != 0:
            # calling setParallelLimit after createSubQueues will
            # cause the subqueues to be recalculated
            self.subqueuedQueue = list()
            self.createSubqueues()

    def createSubqueues(self):
        # splits the input queue in subqueues of the required 
        # size for step processing
        if len(self.queue) == 0:
            raise RuntimeError('must register queue before building subqueues')
        for i in range(0, len(self.queue), self.parallelLimit):
            self.subqueuedQueue.append(self.queue[i:i+self.parallelLimit])
    
    def launch(self):
        # process subqueue by subqueue
        self.createSubqueues()
        for subqueue in tqdm(self.subqueuedQueue):
            # for every subqueue, reset processes list
            processes = list()
            for i in subqueue:
                # launch parallel processing per subqueue
                p = multiprocessing.Process(target=self.stepFunction, args=(i,))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
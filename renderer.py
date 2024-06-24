import multiprocessing
import random

import numpy as np
import rawpy
from tqdm import tqdm
import multiprocessing as mp


class Renderer:
    def __init__(self, num_worker, filename):
        self.num_worker = num_worker
        self.filename = filename
        with rawpy.imread(filename) as raw:
            self.rgb = raw.postprocess()

    def render(self) -> np.array:
        for x in tqdm(range(self.rgb.shape[0]), unit=' rows'):
            for y in range(self.rgb.shape[1]):
                pixel = self.rgb[x][y]
                # print(pixel)
                #if pixel[0] > 100:
                #    pixel[0] = random.randint(0, 255)
                r, g, b = pixel
                self.rgb[x][y] = (r, b, b)
        return self.rgb

    def render_multicore(self):
        height, width, channels = self.rgb.shape

        job_queues = []
        result_queue = multiprocessing.Queue()
        for q in range(0, self.num_worker):
            queue = multiprocessing.Queue()
            job_queues.append(queue)
        worker = []
        for i in range(0, self.num_worker):
            print(f"{i} worker started")
            p = multiprocessing.Process(target=render_worker, args=(job_queues[i], result_queue,))
            worker.append(p)
            p.start()

        for i in range(len(self.rgb)):
            job_queues[i % self.num_worker].put((self.rgb[i], i))

        results = []
        counter = 0
        #while not result_queue.empty():
        while not result_queue.empty() and counter != len(self.rgb):
        #for i in tqdm(range(len(self.rgb)), unit=' rows'):
            results.append(result_queue.get())


        for result in results:
            self.rgb[result[1]] = result[0]
        return self.rgb



def render_worker(job_queue, result_queue):
    while True:
        job = job_queue.get()
        line = job[0]
        index = job[1]
        length = len(line)
        for x in range(length):
            pixel = line[x]
            #print(pixel)
            if pixel[0] > 50:
                pixel[0] = random.randint(0, 255)
                pixel[1] = 0

        result_queue.put((line, index))
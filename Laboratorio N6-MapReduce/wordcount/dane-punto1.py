from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        idemp, sector,salary,year = line.split(',')
        yield idemp, 1

    def reducer(self, idemp, values):
        l = sum(values)
        yield idemp, l

if __name__ == '__main__':
    MRWordFrequencyCount.run()


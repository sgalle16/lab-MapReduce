from mrjob.job import MRJob


class SalaryStatistics(MRJob):

    def mapper(self, _, line):
        idemp, sececon, salary, year = line.strip().split(',')

        if idemp == 'idemp':  # Skip the header line
            return

        try:
            salary = int(salary)

            yield sececon, ('sector_avg', salary)

            yield idemp, ('emp_avg', salary)

            yield idemp, ('sector_count', sececon)

        except ValueError:
            pass

    def reducer(self, key, values):
        total_salary_sector = 0
        count_sector = 0
        total_salary_emp = 0
        count_emp = 0
        sectors = set()

        for value_type, value in values:
            if value_type == 'sector_avg':
                total_salary_sector += value
                count_sector += 1
            elif value_type == 'emp_avg':
                total_salary_emp += value
                count_emp += 1
            elif value_type == 'sector_count':
                sectors.add(value)

        if count_sector > 0:
            avg_salary_sector = total_salary_sector / count_sector
            yield key, {'type': 'sector_avg', 'avg_salary': avg_salary_sector}

        if count_emp > 0:
            avg_salary_emp = total_salary_emp / count_emp
            yield key, {'type': 'emp_avg', 'avg_salary': avg_salary_emp}

        if sectors:
            yield key, {'type': 'sector_count', 'count': len(sectors)}


if __name__ == '__main__':
    SalaryStatistics.run()

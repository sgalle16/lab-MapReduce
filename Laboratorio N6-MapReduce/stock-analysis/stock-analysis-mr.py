from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict


class StockAnalysis(MRJob):

    def mapper(self, _, line):
        company, price, date = line.strip().split(',')
        if company != 'company':
            try:
                price = float(price)
                yield company, (date, price)
            except ValueError:
                pass

    def reducer(self, key, values):
        prices_by_date = defaultdict(list)
        for date, price in values:
            prices_by_date[date].append(price)

        min_date = None
        max_date = None
        min_price = None
        max_price = None
        always_increasing = True
        black_day_count = defaultdict(int)

        dates = sorted(prices_by_date.keys())  # Sort dates chronologically
        for i in range(1, len(dates)):
            prev_date = dates[i - 1]
            curr_date = dates[i]
            prev_avg_price = sum(
                prices_by_date[prev_date]) / len(prices_by_date[prev_date])
            curr_avg_price = sum(
                prices_by_date[curr_date]) / len(prices_by_date[curr_date])
            if prev_avg_price > curr_avg_price:
                always_increasing = False
                break

        for date, price_list in prices_by_date.items():
            avg_price = sum(price_list) / len(price_list)
            if min_price is None or avg_price < min_price:
                min_price = avg_price
                min_date = date
            if max_price is None or avg_price > max_price:
                max_price = avg_price
                max_date = date

            for price in price_list:
                black_day_count[price] += 1

        black_day_price = min(black_day_count, key=black_day_count.get)
        black_day_count = black_day_count[black_day_price]

        yield key, {
            'min_price': min_price,
            'min_date': min_date,
            'max_price': max_price,
            'max_date': max_date,
            'always_increasing': always_increasing,
            'black_day_price': black_day_price,
            'black_day_count': black_day_count
        }

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    StockAnalysis.run()

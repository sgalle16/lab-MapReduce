from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict


class MovieAnalysis(MRJob):

    def mapper(self, _, line):
        user, movie, rating, genre, date = line.strip().split(',')
        if user != 'Usuario':  # Skip the header line
            try:
                user = int(user)
                movie = int(movie)
                rating = int(rating)
                yield user, (movie, rating, genre, date)
            except ValueError:
                pass

    def reducer(self, key, values):
        movies_watched = defaultdict(int)
        total_ratings = defaultdict(int)
        rating_counts = defaultdict(int)
        dates_watched = defaultdict(int)
        genres_watched = defaultdict(set)

        for movie, rating, genre, date in values:
            movies_watched[movie] += 1
            total_ratings[movie] += rating
            rating_counts[movie] += 1
            dates_watched[date] += 1
            genres_watched[genre].add(movie)

        # 1.
        movies_count_avg_rating = {}
        for movie, count in movies_watched.items():
            avg_rating = total_ratings[movie] / rating_counts[movie]
            movies_count_avg_rating[movie] = {
                'count': count, 'avg_rating': avg_rating}

        # 2.
        max_date_watched = max(dates_watched, key=dates_watched.get)

        # 3.
        min_date_watched = min(dates_watched, key=dates_watched.get)

        # 4.
        users_per_movie_avg_rating = {}
        for movie, count in movies_watched.items():
            avg_rating = total_ratings[movie] / rating_counts[movie]
            users_per_movie_avg_rating[movie] = {
                'users_count': count, 'avg_rating': avg_rating}

        # 5.
        worst_avg_rating_date = min(dates_watched, key=dates_watched.get)

        # 6.
        best_avg_rating_date = max(dates_watched, key=dates_watched.get)

        # 7.
        best_worst_movies_genre = {}
        for genre, movies in genres_watched.items():
            best_movie = max(
                movies, key=lambda x: total_ratings[x] / rating_counts[x])
            worst_movie = min(
                movies, key=lambda x: total_ratings[x] / rating_counts[x])
            best_worst_movies_genre[genre] = {
                'best_movie': best_movie, 'worst_movie': worst_movie}

        yield key, {
            'movies_count_avg_rating': movies_count_avg_rating,
            'max_date_watched': max_date_watched,
            'min_date_watched': min_date_watched,
            'users_per_movie_avg_rating': users_per_movie_avg_rating,
            'worst_avg_rating_date': worst_avg_rating_date,
            'best_avg_rating_date': best_avg_rating_date,
            'best_worst_movies_genre': best_worst_movies_genre
        }

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    MovieAnalysis.run()

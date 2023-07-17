import random
from rest_framework import throttling

class BurstRateThrottle(throttling.UserRateThrottle):
    """ Throttle total of requests per minute """
    scope = 'burst'
    rate = '6/min'

    def wait(self):
        return 3

class SustainedRateThrottle(throttling.UserRateThrottle):
    """ Throttle total of requests per day """
    scope = 'sustained'
    rate = '10/day'

    def wait(self):
        return 3

class RandomRateThrottle(throttling.BaseThrottle):
    """ Randomly throttle 1 in every 10 requests """

    scope='random'

    def allow_request(self, request, view):
        num = random.randint(1, 10)
        print(num)
        return num != 1

    def wait(self):
        return 3
from rest_framework.throttling import UserRateThrottle

class ReviewDetailThrottle(UserRateThrottle):
    scope = 'throttling_for_review_details'

class ReviewListThrottle(UserRateThrottle):
    scope = 'throttling_for_review_lists'
# import os
# from inspire_utils.record import get_value


# CLASSIFIER_MAPPING = {
#     "core": "CORE",
#     "non_core": "Non-CORE",
#     "rejected": "Rejected"
# }

# def prepare_classifier_payload(record):
#     """Prepare payload to send to Inspire Classifier."""
#     payload = {
#         'title': get_value(record, 'titles.title[0]', ''),
#         'abstract': get_value(record, 'abstracts.value[0]', ''),
#     }
#     return payload


# def guess_coreness(data):
#     """Workflow task to ask inspire classifier for a coreness assessment."""
#     predictor_url = os.getenv("INSPIRE_CLASSIFIER_URI")
#     if not predictor_url:
#         return

#     payload = prepare_classifier_payload(data)
#     results = prepare_classifier_payload(predictor_url, payload)

#     scores = results["scores"]
#     max_score = scores[results['prediction']]
#     decision = CLASSIFIER_MAPPING[results["prediction"]]
#     scores = {
#         "CORE": scores["core"],
#         "Non-CORE": scores["non_core"],
#         "Rejected": scores["rejected"],
#     }
#     # Generate a normalized relevance_score useful for sorting
#     relevance_score = max_score
#     match decision:
#         case "CORE":
#             relevance_score += 1
#         case "Non-CORE":
#             relevance_score = 0.5 * scores["Non-CORE"] + scores["CORE"]
#         case "Rejected":
#             relevance_score *= -1
#     # We assume a CORE paper to have the highest relevance so we add a
#     # significant value to seperate it from Non-Core and Rejected.
#     # Normally scores range from 0 / +1 so 1 is significant.
#     # Non-CORE scores are untouched, while Rejected is set as negative.
#     # Finally this provides one normalized score of relevance across
#     # all categories of papers.
#     relevance_prediction = dict(
#         max_score=max_score,
#         decision=decision,
#         scores=scores,
#         relevance_score=relevance_score
#     )
#     print(relevance_prediction)

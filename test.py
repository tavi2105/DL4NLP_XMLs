from transformers import pipeline

model_checkpoint = 'bert-base-cased'
model_output_checkpoint = 'transformers/nfl_pbp_token_classifier'

classifier = pipeline(
    'ner',
    model=model_output_checkpoint,
    aggregation_strategy='simple'
)

examples = [
  '(6:51 - 1st) (Shotgun) P.Mahomes scrambles right end to LAC 34 for 2 yards (S.Joseph; K.Van Noy). FUMBLES (S.Joseph), and recovers at LAC 34.',
]

responses = classifier(examples)
print(responses)

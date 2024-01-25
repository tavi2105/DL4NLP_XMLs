import json

from datasets import Dataset
from transformers import DataCollatorForTokenClassification
from extr_ds.manager.utils.filesystem import load_document
import numpy
import evaluate
from transformers.keras_callbacks import KerasMetricCallback
import tensorflow as tf
from transformers import AutoTokenizer, \
    TFAutoModelForTokenClassification

from transformers import pipeline

import warnings
warnings.filterwarnings('ignore')

epochs = 1
model_checkpoint = 'bert-base-cased'
model_output_checkpoint = 'transformers/nfl_pbp_token_classifier'

labels = [
    "abbr",
    "orth",
    "MorfDef",
    "gramGrp",
    "label",
    "citRange",
    "quote",
    "citedRange",
    "hi",
    "RegDef",
    "def",
    "cit",
    "term",
    "norm",
    "form",
    "bibl",
    "usg"
]

label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for i, label in enumerate(labels)}


def align_labels(tokenized_inputs, label_list):
    labels = []
    for word_idx in tokenized_inputs.word_ids(batch_index=0):
        label_id = -100
        if word_idx is not None:
            label = label_list[word_idx]

            label_id = label2id[label]

        labels.append(label_id)
        # previous_word_idx = word_idx

    return labels


def get_dataset(tokenizer, model):
    def tokenize_and_align_labels(record):
        tokenized_inputs = tokenizer(
            record['tokens'],
            truncation=True,
            is_split_into_words=True
        )

        tokenized_inputs['labels'] = align_labels(
            tokenized_inputs,
            record['labels']
        )

        return tokenized_inputs

    ents_dataset = json.loads(
        load_document('dataset/dataset.json')
    )

    # random.shuffle(ents_dataset)

    pivot = int(len(ents_dataset) * .8)
    data_collator = DataCollatorForTokenClassification(
        tokenizer,
        return_tensors='tf'
    )

    train_dataset = Dataset.from_list(ents_dataset[:pivot])
    tf_train_set = model.prepare_tf_dataset(
        train_dataset.map(
            tokenize_and_align_labels,
            batched=False
        ),
        shuffle=True,
        collate_fn=data_collator,
    )

    test_dataset = Dataset.from_list(ents_dataset[pivot:])
    tf_test_set = model.prepare_tf_dataset(
        test_dataset.map(
            tokenize_and_align_labels,
            batched=False
        ),
        shuffle=True,
        collate_fn=data_collator,
    )

    return tf_train_set, tf_test_set


seqeval = evaluate.load('seqeval')


def compute_metrics(preds):
    predictions, actuals = preds
    predictions = numpy.argmax(predictions, axis=2)

    results = seqeval.compute(
        predictions=[
            [labels[p] for p, l in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, actuals)
        ],
        references=[
            [labels[l] for p, l in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, actuals)
        ]
    )

    return {
        key: results[f'overall_{key}']
        for key in ['precision', 'recall', 'f1', 'accuracy']
    }


tokenizer = AutoTokenizer.from_pretrained(
    model_checkpoint
)

model = TFAutoModelForTokenClassification.from_pretrained(
    model_checkpoint,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

tf_train_set, tf_test_set = get_dataset(tokenizer, model)

callbacks = [
    KerasMetricCallback(
        metric_fn=compute_metrics,
        eval_dataset=tf_test_set
    ),
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
]

optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
model.compile(optimizer=optimizer)
model.fit(
    x=tf_train_set,
    validation_data=tf_test_set,
    epochs=epochs,
    callbacks=callbacks
)


classifier = pipeline(
    'ner',
    model=model,
    aggregation_strategy='simple'
)

examples = [
  'DISFAVORITOR, -OÂRE adj. (învechit, rar) Care defavorizează. A tractarisi şi a-şi dobândi oarecare tocmele mai puţin disfavoritoare. AR (1829), 1071/34.     - Pl.: disfavoritori, -oare. — De la disfavoare.',
]

responses = classifier(examples)
print(responses)

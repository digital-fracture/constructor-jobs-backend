import torch
import numpy as np
from catboost import CatBoostClassifier
from transformers import BertModel, BertTokenizer

from misc.constants import weights_path


class TextDetectionModel:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model_name = "DeepPavlov/rubert-base-cased"
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.bert_model = BertModel.from_pretrained(model_name).to(self.device)

        self.cat_boost_model = CatBoostClassifier()
        self.cat_boost_model.load_model(weights_path, format="cbm")

    def get_texts_proba(self, texts: list[str]) -> np.array:
        token_ids = self.tokenizer(texts, padding=True)["input_ids"]
        input_ids = torch.tensor(token_ids).to(self.device)
        with torch.no_grad():
            outputs = self.bert_model(input_ids)
            sentences_embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
        cpu_bert_embeddings = np.array(
            [np.array(txt.cpu()) for txt in sentences_embeddings]
        )
        return self.cat_boost_model.predict_proba(cpu_bert_embeddings)

    @staticmethod
    def __get_sentences(text: list[str], context_size: int = 2) -> list[str]:
        sentences = list()
        for ind in range(len(text)):
            words = text[max(ind - context_size - 1, 0):min(ind + context_size + 1, len(text) - 1)]
            sentence = " ".join(words)
            sentences.append(sentence)
        return sentences

    def classify_text(self, text: str, context_size: int, confidence_level: float) -> dict[str, str]:
        answer = dict()
        requirements = list()
        terms = list()
        notes = list()
        results_labels = list()
        text = text.split()
        sentences = self.__get_sentences(text, context_size)

        _sentences_probs = self.get_texts_proba(sentences)

        for ind in range(len(text)):
            probs = _sentences_probs[ind]
            class_index = probs.argmax() + 1
            probability = probs[class_index - 1]
            if class_index == 1 and probability >= confidence_level:
                requirements.append(text[ind])
                results_labels.append(1)
            elif class_index == 2 and probability >= confidence_level:
                terms.append(text[ind])
                results_labels.append(2)
            elif class_index == 3 and probability >= confidence_level:
                notes.append(text[ind])
                results_labels.append(3)
            else:
                results_labels.append(0)
        answer["requirements"] = " ".join(requirements).replace("Требования: ", "").replace("требования: ", "")
        answer["conditions"] = " ".join(terms).replace("Условия: ", "").replace("условия: ", "")
        answer["notes"] = " ".join(notes).replace("Примечания: ", "").replace("примечания: ", "")

        return answer

    def predict(self, text: str, context_size: int = 15, confidence_level: float = 0.55):
        return self.classify_text(text, context_size, confidence_level)


model = TextDetectionModel()

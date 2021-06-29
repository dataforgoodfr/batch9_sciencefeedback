from abc import ABC
import json
import logging
import os
import ast
import torch
import zipfile
from transformers import AutoModel, AutoTokenizer

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)


class TransformersClassifierHandler(BaseHandler, ABC):
    """
    Transformers handler class for embedding
    """
    def __init__(self):
        super(TransformersClassifierHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)

        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        #read configs for the mode, model_name, etc. from setup_config.json
        self.model = AutoModel.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)


        self.model.to(self.device)
        self.model.eval()

        logger.debug('Transformer model from path {0} loaded successfully'.format(model_dir))

        # Read the mapping file, index to object name
        mapping_file_path = os.path.join(model_dir, "index_to_name.json")
        # Question answering does not need the index_to_name.json file.

        self.initialized = True

    def preprocess(self, requests):
        logger.debug(requests)
        inputs = requests[0].get("data")
        if inputs is None:
            inputs = requests[0].get("body")

        #sentences = inputs.decode('utf-8')
        logger.info("Received text: '%s'", inputs)

        token_keyword = torch.tensor(self.tokenizer.encode(inputs)).unsqueeze(0)
        return token_keyword

    def inference(self, inputs):
        """
            Encode claim and corpus documents

            - claim is str
            - corpus : [[str1, str2, str3 ...], [str1, str2, str3 ...], ...]
        """
        return self.model(inputs)


    def postprocess(self, result):
        result = {
            'embedding': result[0][0][1:-1].detach().numpy().mean(axis=0).tolist()
        }
        return [json.dumps(result)]


_service = TransformersClassifierHandler()


def handle(data, context):
    try:
        if not _service.initialized:
            _service.initialize(context)

        if data is None:
            return None

        inputs = _service.preprocess(data)
        inference_result = _service.inference(inputs)
        result = _service.postprocess(inference_result)

        return result
    except Exception as e:
        print(e)
        error = {'error': str(e)}
        return [json.dumps(error)]

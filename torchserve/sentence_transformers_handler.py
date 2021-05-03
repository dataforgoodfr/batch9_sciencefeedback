from abc import ABC
import json
import logging
import os
import ast
import torch
from ts.torch_handler.base_handler import BaseHandler
from sentence_transformers import SentenceTransformer, util
import zipfile


logger = logging.getLogger(__name__)


def decode(l):
    if isinstance(l, list):
        return [decode(x) for x in l]
    else:
        return l.decode('utf-8')

class TransformersSeqClassifierHandler(BaseHandler, ABC):
    """
    Transformers handler class for sequence, token classification and question answering.
    """
    def __init__(self):
        super(TransformersSeqClassifierHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        serialized_file = self.manifest['model']['serializedFile']
        model_pt_path = os.path.join(model_dir, serialized_file)
        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")
        with zipfile.ZipFile(model_dir + '/model.pt', 'r') as zip_ref:
            zip_ref.extractall(model_dir)

        with zipfile.ZipFile(model_dir + '/pool.zip', 'r') as zip_ref:
            zip_ref.extractall(model_dir)

        #read configs for the mode, model_name, etc. from setup_config.json
        self.model = SentenceTransformer(model_dir)


        self.model.to(self.device)
        self.model.eval()

        logger.debug('Transformer model from path {0} loaded successfully'.format(model_dir))

        # Read the mapping file, index to object name
        mapping_file_path = os.path.join(model_dir, "index_to_name.json")
        # Question answering does not need the index_to_name.json file.

        self.initialized = True

    def preprocess(self, requests):
        """
            The input is json type with :
            {
                'claim': str,
                'corpus': [[str1, str2, str3 ...], [str1, str2, str3 ...], ...]
            }
        """
        inputs = requests[0].get("data")
        if inputs is None:
            inputs = requests[0].get("body")
        return inputs

    def inference(self, inputs):
        """
            Encode claim and corpus documents

            - claim is str
            - corpus : [[str1, str2, str3 ...], [str1, str2, str3 ...], ...]
        """

        return self.model.encode(inputs)


    def postprocess(self, result):

        result = {
            'embedding': result.tolist()
        }
        return [json.dumps(result)]


_service = TransformersSeqClassifierHandler()


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
        error = {'error': str(e)}
        return [json.dumps(error)]

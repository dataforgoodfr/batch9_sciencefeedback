cd /home/model-server/

torch-model-archiver --model-name bert --version 1.0 --serialized-file ./sentence_model/pytorch_model.bin --extra-files "./sentence_model/config.json,./sentence_model/vocab.txt" --handler "./transformers_handler.py"

mv bert.mar model-store/

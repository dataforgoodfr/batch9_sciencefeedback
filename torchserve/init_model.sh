cd /home/model-server/

torch-model-archiver --model-name stsbrobertabase \
-v 1.0 --serialized-file sentence_model/model.pt \
--handler ./sentence_transformers_handler.py \
--extra-files "sentence_model/config.json,sentence_model/pool.zip,sentence_model/modules.json"

mv stsbrobertabase.mar model-store/

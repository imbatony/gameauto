import time
from .utils import get_logger
from cnocr import CnOcr

logger = get_logger(__name__, {})
logger.info("加载ocr模型,请稍等...")

_start_time = time.time()
# 所有参数都使用默认值
cnocr = CnOcr(
    rec_model_name="densenet_lite_136-gru",
    det_model_name="db_shufflenet_v2_small",
    det_more_configs={"rotated_bbox": False},
)
_ellipsis = time.time() - _start_time
logger.info(f"加载完成,耗时{_ellipsis:.2f}秒")

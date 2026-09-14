"""Util logic shared by all eval modules"""

from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

from agno.utils.log import logger

if TYPE_CHECKING:
    from agno.eval.accuracy import AccuracyResult
    from agno.eval.performance import PerformanceResult
    from agno.eval.reliability import ReliabilityResult


def store_result_in_file(
    file_path: str,
    result: Union["AccuracyResult", "PerformanceResult", "ReliabilityResult"],
    eval_id: Optional[str] = None,
    name: Optional[str] = None,
):
    """Store the given result in the given file path"""
    try:
        import json

        fn_path = Path(file_path.format(name=name, eval_id=eval_id))
        if not fn_path.parent.exists():
            fn_path.parent.mkdir(parents=True, exist_ok=True)
        fn_path.write_text(json.dumps(asdict(result), indent=4))
    except Exception as e:
        logger.warning(f"Failed to save result to file: {e}")


def log_eval_run(
    run_id: str,
    run_data: dict,
    eval_type,
    agent_id: str | None = None,
    model_id: str | None = None,
    model_provider: str | None = None,
    name: str | None = None,
    evaluated_entity_name: str | None = None,
    team_id: str | None = None,
) -> None:
    """Log evaluation run to the Agno platform."""
    pass

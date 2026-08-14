"""Captures reproducibility metadata (who/when/what code) alongside a recorded run."""

import datetime
import getpass
import socket
import subprocess
from pathlib import Path

import yaml


def _git_commit_hash(repo_path: Path) -> str:
    try:
        return subprocess.check_output(
            ['git', '-C', str(repo_path), 'rev-parse', 'HEAD'],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return 'unknown'


def _git_dirty(repo_path: Path) -> bool:
    try:
        status = subprocess.check_output(
            ['git', '-C', str(repo_path), 'status', '--porcelain'],
            text=True, stderr=subprocess.DEVNULL,
        )
        return bool(status.strip())
    except Exception:
        return False


def write_metadata(
    output_dir: Path,
    experiment_name: str,
    notes: str = '',
    repo_path: Path = None,
) -> Path:
    """Write metadata.yaml describing this experiment run into output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        'experiment_name': experiment_name,
        'notes': notes,
        'timestamp': datetime.datetime.now().isoformat(),
        'operator': getpass.getuser(),
        'hostname': socket.gethostname(),
    }

    if repo_path is not None:
        metadata['code_commit'] = _git_commit_hash(repo_path)
        metadata['code_dirty'] = _git_dirty(repo_path)

    metadata_path = output_dir / 'metadata.yaml'
    with open(metadata_path, 'w') as f:
        yaml.safe_dump(metadata, f, sort_keys=False)

    return metadata_path

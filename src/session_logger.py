"""
セッション結果のログ保存モジュール
"""

import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sessions")


def ensure_data_dir() -> None:
    """データディレクトリを作成"""
    os.makedirs(DATA_DIR, exist_ok=True)


def get_csv_path(mode: str) -> str:
    """モード別のCSVパスを取得"""
    ensure_data_dir()
    return os.path.join(DATA_DIR, f"{mode}.csv")


def save_tracking_session(t0_rate: float, duration: float) -> bool:
    """
    Trackingセッションの結果を保存
    
    Args:
        t0_rate: T0率 (%)
        duration: セッション時間 (秒)
    """
    csv_path = get_csv_path("tracking")
    file_exists = os.path.exists(csv_path)
    
    try:
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # ヘッダー
            if not file_exists:
                writer.writerow(['timestamp', 'mode', 't0_rate', 'duration'])
            
            writer.writerow([
                datetime.now().isoformat(),
                'tracking',
                f"{t0_rate:.2f}",
                f"{duration:.1f}"
            ])
        return True
    except Exception as e:
        print(f"セッション保存エラー: {e}")
        return False


def save_flicking_session(
    accuracy: float,
    avg_reaction: float,
    min_reaction: float,
    hits: int,
    total: int
) -> bool:
    """
    Flickingセッションの結果を保存
    
    Args:
        accuracy: 命中率 (%)
        avg_reaction: 平均反応速度 (ms)
        min_reaction: 最速反応速度 (ms)
        hits: ヒット数
        total: 総ターゲット数
    """
    csv_path = get_csv_path("flicking")
    file_exists = os.path.exists(csv_path)
    
    try:
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # ヘッダー
            if not file_exists:
                writer.writerow([
                    'timestamp', 'mode', 'accuracy',
                    'avg_reaction_ms', 'min_reaction_ms', 'hits', 'total'
                ])
            
            writer.writerow([
                datetime.now().isoformat(),
                'flicking',
                f"{accuracy:.1f}",
                f"{avg_reaction:.0f}" if avg_reaction > 0 else "",
                f"{min_reaction:.0f}" if min_reaction > 0 else "",
                hits,
                total
            ])
        return True
    except Exception as e:
        print(f"セッション保存エラー: {e}")
        return False


def load_tracking_sessions(limit: int = 20) -> List[Dict[str, Any]]:
    """Trackingセッション履歴を読み込み"""
    csv_path = get_csv_path("tracking")
    sessions = []
    
    if not os.path.exists(csv_path):
        return sessions
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sessions.append({
                    'timestamp': row['timestamp'],
                    'mode': row['mode'],
                    't0_rate': float(row['t0_rate']),
                    'duration': float(row['duration'])
                })
    except Exception as e:
        print(f"セッション読み込みエラー: {e}")
    
    return sessions[-limit:]


def load_flicking_sessions(limit: int = 20) -> List[Dict[str, Any]]:
    """Flickingセッション履歴を読み込み"""
    csv_path = get_csv_path("flicking")
    sessions = []
    
    if not os.path.exists(csv_path):
        return sessions
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sessions.append({
                    'timestamp': row['timestamp'],
                    'mode': row['mode'],
                    'accuracy': float(row['accuracy']),
                    'avg_reaction_ms': float(row['avg_reaction_ms']) if row['avg_reaction_ms'] else 0,
                    'min_reaction_ms': float(row['min_reaction_ms']) if row['min_reaction_ms'] else 0,
                    'hits': int(row['hits']),
                    'total': int(row['total'])
                })
    except Exception as e:
        print(f"セッション読み込みエラー: {e}")
    
    return sessions[-limit:]


def get_tracking_stats() -> Dict[str, Any]:
    """Tracking統計を取得"""
    sessions = load_tracking_sessions(100)
    
    if not sessions:
        return {'count': 0, 'avg': 0, 'best': 0, 'recent': []}
    
    t0_rates = [s['t0_rate'] for s in sessions]
    
    return {
        'count': len(sessions),
        'avg': sum(t0_rates) / len(t0_rates),
        'best': max(t0_rates),
        'recent': [s['t0_rate'] for s in sessions[-10:]]
    }


def get_flicking_stats() -> Dict[str, Any]:
    """Flicking統計を取得"""
    sessions = load_flicking_sessions(100)
    
    if not sessions:
        return {'count': 0, 'avg_acc': 0, 'best_acc': 0, 'avg_reaction': 0, 'recent': []}
    
    accuracies = [s['accuracy'] for s in sessions]
    reactions = [s['avg_reaction_ms'] for s in sessions if s['avg_reaction_ms'] > 0]
    
    return {
        'count': len(sessions),
        'avg_acc': sum(accuracies) / len(accuracies),
        'best_acc': max(accuracies),
        'avg_reaction': sum(reactions) / len(reactions) if reactions else 0,
        'recent': [s['accuracy'] for s in sessions[-10:]]
    }

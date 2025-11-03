"""
HexStrike API Module
Flask blueprints and API endpoints
"""

# 尝试导入优化路由
try:
    from api.routes.optimization import register_optimization_routes
    OPTIMIZATION_ROUTES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_ROUTES_AVAILABLE = False

__all__ = []

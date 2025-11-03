#!/usr/bin/env python3
"""
HexStrike AI - Optimization API Routes
优化功能API路由

提供性能优化、AI智能决策、高级功能的HTTP API接口
"""

from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
optimization_bp = Blueprint('optimization', __name__, url_prefix='/api/optimization')


@optimization_bp.route('/status', methods=['GET'])
def get_optimization_status():
    """
    获取优化模块状态
    GET /api/optimization/status
    """
    try:
        # 尝试导入优化模块
        try:
            from advanced_features import PentestChain, IntelligentFuzzer, CTFSolver
            from ai_intelligence import IntelligentRecommender, LearningSystem
            from performance_optimizer import LazyToolLoader, SmartCache, ParallelExecutor
            
            status = {
                'enabled': True,
                'modules': {
                    'advanced_features': True,
                    'ai_intelligence': True,
                    'performance_optimizer': True
                },
                'features': {
                    'pentest_chain': True,
                    'intelligent_fuzzer': True,
                    'ctf_solver': True,
                    'ai_recommender': True,
                    'learning_system': True,
                    'lazy_loading': True,
                    'smart_caching': True,
                    'parallel_execution': True
                }
            }
        except ImportError as e:
            status = {
                'enabled': False,
                'error': str(e),
                'modules': {},
                'features': {}
            }
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"❌ Error getting optimization status: {e}")
        return jsonify({'error': str(e)}), 500


@optimization_bp.route('/ai/analyze', methods=['POST'])
def ai_analyze_request():
    """
    AI智能分析用户请求
    POST /api/optimization/ai/analyze
    
    Body: {
        "user_input": "扫描 192.168.1.1 的端口",
        "context": {"speed": "fast"}
    }
    """
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        context = data.get('context', {})
        
        if not user_input:
            return jsonify({'error': 'user_input is required'}), 400
        
        # 使用AI推荐器分析
        try:
            from ai_intelligence import IntelligentRecommender
            recommender = IntelligentRecommender()
            result = recommender.process_request(user_input, context)
            
            return jsonify({
                'success': True,
                'analysis': result
            }), 200
            
        except ImportError:
            return jsonify({
                'error': 'AI Intelligence module not available',
                'hint': 'Run: python install_optimizations.py'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Error in AI analysis: {e}")
        return jsonify({'error': str(e)}), 500


@optimization_bp.route('/pentest/chain', methods=['POST'])
def create_pentest_chain():
    """
    创建渗透测试链
    POST /api/optimization/pentest/chain
    
    Body: {
        "target": "example.com",
        "objective": "comprehensive"
    }
    """
    try:
        data = request.get_json()
        target = data.get('target', '')
        objective = data.get('objective', 'comprehensive')
        
        if not target:
            return jsonify({'error': 'target is required'}), 400
        
        try:
            from advanced_features import PentestChain
            
            # 创建渗透测试链
            chain = PentestChain(target, objective)
            
            return jsonify({
                'success': True,
                'chain': {
                    'target': chain.target,
                    'objective': chain.objective,
                    'phases': chain.PHASES,
                    'status': 'created'
                }
            }), 200
            
        except ImportError:
            return jsonify({
                'error': 'Advanced Features module not available',
                'hint': 'Run: python install_optimizations.py'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Error creating pentest chain: {e}")
        return jsonify({'error': str(e)}), 500


@optimization_bp.route('/fuzzer/scan', methods=['POST'])
def intelligent_fuzzer_scan():
    """
    智能Fuzzer扫描
    POST /api/optimization/fuzzer/scan
    
    Body: {
        "target_url": "https://example.com/api",
        "attack_type": "sql_injection",
        "parameters": ["id", "user"]
    }
    """
    try:
        data = request.get_json()
        target_url = data.get('target_url', '')
        attack_type = data.get('attack_type', 'all')
        parameters = data.get('parameters')
        
        if not target_url:
            return jsonify({'error': 'target_url is required'}), 400
        
        try:
            from advanced_features import IntelligentFuzzer
            
            # 创建智能Fuzzer
            fuzzer = IntelligentFuzzer(target_url)
            results = fuzzer.fuzz(attack_type, parameters)
            
            return jsonify({
                'success': True,
                'results': results
            }), 200
            
        except ImportError:
            return jsonify({
                'error': 'Advanced Features module not available'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Error in fuzzer scan: {e}")
        return jsonify({'error': str(e)}), 500


@optimization_bp.route('/ctf/solve', methods=['POST'])
def ctf_solve_challenge():
    """
    CTF自动解题
    POST /api/optimization/ctf/solve
    
    Body: {
        "name": "Easy Crypto",
        "category": "crypto",
        "description": "Decode this...",
        "data": "ZmxhZ3t0ZXN0fQ=="
    }
    """
    try:
        data = request.get_json()
        
        try:
            from advanced_features import CTFSolver
            
            # 创建CTF解题器
            solver = CTFSolver()
            result = solver.auto_solve(data)
            
            return jsonify({
                'success': True,
                'result': result
            }), 200
            
        except ImportError:
            return jsonify({
                'error': 'Advanced Features module not available'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Error solving CTF: {e}")
        return jsonify({'error': str(e)}), 500


@optimization_bp.route('/cache/stats', methods=['GET'])
def get_cache_stats():
    """
    获取缓存统计信息
    GET /api/optimization/cache/stats
    """
    try:
        try:
            from performance_optimizer import SmartCache
            
            # 这里可以从全局实例获取统计
            stats = {
                'cache_available': True,
                'note': 'Cache statistics from global instance'
            }
            
            return jsonify(stats), 200
            
        except ImportError:
            return jsonify({
                'error': 'Performance Optimizer module not available'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Error getting cache stats: {e}")
        return jsonify({'error': str(e)}), 500


@optimization_bp.route('/learning/record', methods=['POST'])
def record_learning_data():
    """
    记录学习数据
    POST /api/optimization/learning/record
    
    Body: {
        "tool": "nmap",
        "success": true,
        "duration": 5.2,
        "target_type": "ip"
    }
    """
    try:
        data = request.get_json()
        
        try:
            from ai_intelligence import LearningSystem
            
            learning_system = LearningSystem()
            learning_system.record_scan(data)
            
            return jsonify({
                'success': True,
                'message': 'Learning data recorded'
            }), 200
            
        except ImportError:
            return jsonify({
                'error': 'AI Intelligence module not available'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Error recording learning data: {e}")
        return jsonify({'error': str(e)}), 500


def register_optimization_routes(app):
    """注册优化路由到Flask应用"""
    app.register_blueprint(optimization_bp)
    logger.info("✅ Optimization routes registered")

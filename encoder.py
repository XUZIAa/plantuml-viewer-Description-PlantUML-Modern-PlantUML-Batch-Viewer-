"""
PlantUML 编码器模块
负责将 PlantUML 代码编码为服务器可识别的格式
"""

import zlib


class PlantUMLEncoder:
    """PlantUML 编码器"""
    
    PLANTUML_ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    
    @classmethod
    def encode(cls, plantuml_text: str) -> str:
        """将 PlantUML 代码编码为 URL 参数"""
        compressed = zlib.compress(plantuml_text.encode('utf-8'))[2:-4]
        return cls._encode64(compressed)
    
    @classmethod
    def _encode64(cls, data: bytes) -> str:
        """PlantUML 专用的 Base64 编码"""
        result = []
        i = 0
        
        while i < len(data):
            if i + 2 < len(data):
                # 处理3个字节
                b1, b2, b3 = data[i], data[i + 1], data[i + 2]
                result.append(cls._encode6bit(b1 >> 2))
                result.append(cls._encode6bit(((b1 & 0x3) << 4) | (b2 >> 4)))
                result.append(cls._encode6bit(((b2 & 0xF) << 2) | (b3 >> 6)))
                result.append(cls._encode6bit(b3 & 0x3F))
                i += 3
            elif i + 1 < len(data):
                # 处理2个字节
                b1, b2 = data[i], data[i + 1]
                result.append(cls._encode6bit(b1 >> 2))
                result.append(cls._encode6bit(((b1 & 0x3) << 4) | (b2 >> 4)))
                result.append(cls._encode6bit((b2 & 0xF) << 2))
                i += 2
            else:
                # 处理1个字节
                b1 = data[i]
                result.append(cls._encode6bit(b1 >> 2))
                result.append(cls._encode6bit((b1 & 0x3) << 4))
                i += 1
        
        return ''.join(result)
    
    @classmethod
    def _encode6bit(cls, b: int) -> str:
        """将6位数据编码为字符"""
        if b < 0 or b > 63:
            return '?'
        return cls.PLANTUML_ALPHABET[b]

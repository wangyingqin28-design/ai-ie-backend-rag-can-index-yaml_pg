# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/utils/snowflake_generator.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
import secrets
import string
import time
from uuid6 import uuid7
# 项目元年时间戳
START_TIMESTAMP = 1444444444444

# 机器ID bit位数
MACHINE_ID_BITS = 4

# 服务ID bit位数
SERVICE_ID_BITS = 3

# 序号 bit位数
SEQUENCE_BITS = 5

# 机器ID最大值计算
MAX_MACHINE_ID = (1 << MACHINE_ID_BITS) - 1

# 服务ID最大值计算
MAX_SERVICE_ID = (1 << SERVICE_ID_BITS) - 1

# 序号掩码最大值
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

# 移位偏移值计算
SERVICE_ID_SHIFT = SEQUENCE_BITS
MACHINE_ID_SHIFT = SEQUENCE_BITS + SERVICE_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + SERVICE_ID_BITS + MACHINE_ID_BITS


class SnowFlake:
    """
    用于生成IDs
    """

    def __init__(self, machine_id=1, service_id=1, sequence=0):
        """
        初始化
        :param machine_id: 机器ID
        :param service_id: 服务ID
        :param sequence: 序号掩码
        """
        # 校验机器ID
        if machine_id > MAX_MACHINE_ID or machine_id < 0:
            raise ValueError('机器ID值越界')

        # 校验服务ID
        if service_id > MAX_SERVICE_ID or service_id < 0:
            raise ValueError('服务ID值越界')

        self.machine_id = machine_id
        self.service_id = service_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def generate_id(self):
        """
        生成ID
        :return:int
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if (self.last_timestamp - timestamp) > 3:
            raise Exception('时钟回拨')
        if self.last_timestamp > timestamp:
            timestamp = self._til_next_millis(self.last_timestamp)

        if timestamp == self.last_timestamp:
            self.sequence = self.sequence + 1
            if self.sequence > MAX_SEQUENCE:
                timestamp = self._til_next_millis(self.last_timestamp)
                self.sequence = 0
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 核心计算
        new_id = ((timestamp - START_TIMESTAMP) << TIMESTAMP_LEFT_SHIFT) | (self.machine_id << MACHINE_ID_SHIFT) | \
                 (self.service_id << SERVICE_ID_SHIFT) | self.sequence

        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


# Global instance
snowflake = SnowFlake()
SAFE_ID_ALPHABET = string.ascii_letters + string.digits + "-_"

#安全字符串
def generate_secure_id(length: int = 32) -> str:
    """
    生成安全字符串 ID。

    包含：
    - 大写字母
    - 小写字母
    - 数字
    - 特殊字符：- _

    示例：
    Ab9_xK2Lm-Pq7Rt5Nw3Yz8Vc
    """
    if length <= 0:
        raise ValueError("length must be greater than 0")

    return "".join(secrets.choice(SAFE_ID_ALPHABET) for _ in range(length))


class SecureIdGenerator:
    def generate_id(self, length: int = 32) -> str:
        return generate_secure_id(length)


secure_id = SecureIdGenerator()

#uuid7的生成
def generate_uuid7_id() -> str:
    return uuid7().hex

if __name__ == '__main__':
    worker = SnowFlake()
    start_timestamp = int(time.time() * 1000)
    for i in range(100):
        print(worker.generate_id())
        print(worker.generate_id())
    end_timestamp = int(time.time() * 1000)
    waste_time = (end_timestamp - start_timestamp) / 1000
    print(waste_time)
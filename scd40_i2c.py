#!/usr/bin/env python3
"""
SCD41 CO2センサー用サンプルコード
定期測定を開始したあと, 1度だけ結果を読み出して表示し, 定期測定を終了する. 
Indoor Corgi, https://www.indoorcorgielec.com
GitHub: https://github.com/IndoorCorgi/cgsensor

必要環境:
1) Raspberry Pi OS, Python3
2) I2Cインターフェース
  Raspberry PiでI2Cを有効にして下さい
  https://www.indoorcorgielec.com/resources/raspberry-pi/raspberry-pi-i2c/

3) 拡張基板
  RPZ-CO2-Sensor: https://www.indoorcorgielec.com/products/rpz-co2-sensor/

4) cgsensorパッケージ
  sudo python3 -m pip install -U cgsensor
"""

import cgsensor  # インポート
import time

from retry import retry

from influxdb import InfluxDBClient
client = InfluxDBClient('192.168.1.180', 8086, 'root', '', 'sensor')


@retry(exceptions=cgsensor.scd41.CRCMismatchError, tries=9999999, delay=5)
def measurement_rt():
    scd40 = cgsensor.SCD41()  # SCD41制御クラスのインスタンス
    # scd40.start_periodic_measurement()  # 5秒おきの定期測定を開始
    while True:
        scd40.read_measurement(timeout=10)  # 測定完了を待ってから測定結果の読み出し
        print('CO2濃度 {}ppm'.format(scd40.co2))  # CO2濃度を取得して表示
        wp_body = [{"measurement": "SCD40_measure",
                    "fields": {"CO2(ppm)": scd40.co2}}]
        client.write_points(wp_body)
        time.sleep(4.8)
    scd41.stop_periodic_measurement()  # 定期測定を終了


if __name__ == '__main__':
    measurement_rt()

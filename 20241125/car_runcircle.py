from pxr import Usd, UsdGeom, Gf
import math

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("20241125/car_runcircle.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())  # 設定 "/World" 為 default prim

# 引用外部的 USD 檔案
asset_prim_path = "/World/ExampleCar"  # 指定引入的位置
asset_prim = stage.DefinePrim(asset_prim_path, "Xform")  # 建立容器
references = asset_prim.GetReferences()  # 獲取 references 接口
references.AddReference('../asset/car.usdz')  # 加入參考 (跳出資料夾)

# 動畫設置：讓車子繞圈圈
asset_xform = UsdGeom.Xformable(asset_prim)

# 半徑設定 (可以根據需要調整)
radius = 5000
# 繞圈總時間幀數 (可以根據需要增加更多的幀)
total_time = 60

# 設置繞圈移動的 Translate 和 RotateY 操作
translate_op = asset_xform.AddTranslateOp()
rotate_op = asset_xform.AddRotateYOp()

# 循環設定每一幀的位移和旋轉
for frame in range(total_time + 1):
    # 計算每個時間點的角度 (角度範圍 0 到 360 度)
    angle_deg = (frame / total_time) * 360
    angle_rad = math.radians(angle_deg)

    # 計算車子的 x 和 z 位置
    x = radius * math.cos(angle_rad)
    z = radius * math.sin(angle_rad)

    # 設置 Translate 值
    translate_op.Set(time=frame, value=(x, 0, z))

    # 設置車子面向的方向，讓它隨著角度變化
    rotate_op.Set(time=frame, value=-angle_deg)

# 保存 USD 檔案
stage.GetRootLayer().Save()

print("USD 檔案已成功創建，車子會繞圈圈動畫效果：looping_car_circle.usd")

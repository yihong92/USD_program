from pxr import Usd, UsdGeom

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("20241125/car_move.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())  # 設定 "/World" 為 default prim

# 引用外部的 USD 檔案
asset_prim_path = "/World/ExampleAsset"  # 指定引入的位置
asset_prim = stage.DefinePrim(asset_prim_path, "Xform")  # 建立容器
references = asset_prim.GetReferences()  # 獲取 references 接口
references.AddReference('../asset/car.usdz')  # 加入參考 # 跳出資料夾../

# 動畫設置：將引用物件移動
asset_xform = UsdGeom.Xformable(asset_prim)

# Add Translate operation to the Xform
translate_op = asset_xform.AddTranslateOp()

# Loop to set translation values from (0, 0, 0) to (0, 0, 10000)
for time in range(0, 21):  # Time goes from 0 to 20
    value = (0, 0, time * 500)  # Increase by 500 each step
    translate_op.Set(time=time, value=value)



# 保存 USD 檔案
stage.GetRootLayer().Save()

print("USD 檔案已成功創建，並加入循環動畫效果：looping_car.usd")
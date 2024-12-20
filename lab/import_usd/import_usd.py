from pxr import Usd, UsdGeom

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("import_usd/import_usd.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())  # 設定 "/World" 為 default prim

# 引用外部的 USD 檔案
asset_prim_path = "/World/ExampleAsset"  # 指定引入的位置
asset_prim = stage.DefinePrim(asset_prim_path, "Xform")  # 建立容器
references = asset_prim.GetReferences()  # 獲取 references 接口
references.AddReference('../asset/lab_table.usdz')  # 加入參考

# 將引用物件移動到場景中某個位置
asset_xform = UsdGeom.Xformable(asset_prim)
asset_xform.AddTranslateOp().Set((20, 0, 0))  # 將引用物件移到 (20, 0, 0)


# 添加調整大小操作
asset_xform.AddScaleOp().Set((100, 100, 100))  # 將引用物件縮放為原來的 100 倍

# 保存 USD 檔案
stage.GetRootLayer().Save()

print("USD 檔案已成功創建，並引入外部物件且可調整大小：simple_scene.usd")

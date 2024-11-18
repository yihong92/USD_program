from pxr import Usd, UsdGeom

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("cube.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World") 
stage.SetDefaultPrim(world.GetPrim())  # 設定 "/World" 為 default prim

cube = UsdGeom.Cube.Define(stage, "/World/cube") # 創建一個立方體
cube.GetSizeAttr().Set(10) # 設定立方體的大小 
xform = UsdGeom.Xform.Define(stage, "/World")
xform.AddTranslateOp().Set((0, 0, 0))  # 將立方體的位置設定為原點 # 設定立方體的位置



# 保存 USD 檔案
stage.GetRootLayer().Save()

print("USD 檔案已成功創建並設置 default prim：simple_scene.usd")


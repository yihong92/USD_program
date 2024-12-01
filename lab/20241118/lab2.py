from pxr import Usd, UsdGeom, Gf

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("20241118/lab_gpt_origal_generate.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())  # 設定 "/World" 為 default prim

# 參數設置
x_spacing = 150  # 桌子之間 X 軸的間距
y_spacing = 100  # 桌子之間 Y 軸的間距
rows = 5        # 總共有 5 排
columns = 5     # 每排有 5 張桌子
table_scale = (0.5, 0.5, 0.5)  # 桌子縮放比例 (X, Y, Z)
computer_scale = (0.3, 0.3, 0.3)  # 電腦縮放比例
chair_scale = (0.5, 0.5, 0.5)  # 椅子縮放比例
cabinet_scale = (1, 1, 1)  # 櫃子縮放比例

# 電腦和椅子的旋轉角度
computer_rotation = Gf.Vec3d(90, 0, 0)  # 電腦旋轉 90 度
chair_rotation = Gf.Vec3d(90, 0, 0)  # 椅子旋轉 90 度

# 創建桌子、電腦和椅子的排列
for row in range(rows):
    for column in range(columns):
        # 計算每張桌子的座標
        x_position = column * x_spacing
        y_position = row * y_spacing
        position = (x_position, y_position, 0)

        # 創建容器 Prim 並添加引用桌子
        table_name = f"Table_{row + 1}_{column + 1}"  # e.g., Table_1_1, Table_1_2
        table_path = f"/World/{table_name}"
        table_prim = stage.DefinePrim(table_path, "Xform")  # 創建容器 Prim
        references = table_prim.GetReferences()  # 獲取引用接口
        references.AddReference('../asset/table.usdz')  # 引用外部桌子

        # 移動每張桌子到正確位置
        table_xform = UsdGeom.Xformable(table_prim)
        table_xform.AddTranslateOp().Set(position)
        table_xform.AddScaleOp().Set(table_scale)

        # 添加電腦到桌子上
        computer_name = f"Computer_{row + 1}_{column + 1}"
        computer_path = f"{table_path}/{computer_name}"
        computer_prim = stage.DefinePrim(computer_path, "Xform")
        computer_references = computer_prim.GetReferences()
        computer_references.AddReference('../asset/computer.usdz')

        # 電腦位置調整和旋轉
        computer_xform = UsdGeom.Xformable(computer_prim)
        computer_xform.AddTranslateOp().Set((0, 0, 50))  # 電腦在桌子上方
        computer_xform.AddScaleOp().Set(computer_scale)
        computer_xform.AddRotateXYZOp().Set(computer_rotation)

        # 添加椅子在桌子前面
        chair_name = f"Chair_{row + 1}_{column + 1}"
        chair_path = f"{table_path}/{chair_name}"
        chair_prim = stage.DefinePrim(chair_path, "Xform")
        chair_references = chair_prim.GetReferences()
        chair_references.AddReference('../asset/chair.usdz')

        # 椅子位置調整和旋轉
        chair_xform = UsdGeom.Xformable(chair_prim)
        chair_xform.AddTranslateOp().Set((0, -30, 0))  # 椅子在桌子前面
        chair_xform.AddScaleOp().Set(chair_scale)
        chair_xform.AddRotateXYZOp().Set(chair_rotation)

# 添加櫃子在右側
cabinet_positions = [(800, 100, 0), (800, 300, 0)]  # 櫃子的位置
for i, pos in enumerate(cabinet_positions):
    cabinet_name = f"Cabinet_{i + 1}"
    cabinet_path = f"/World/{cabinet_name}"
    cabinet_prim = stage.DefinePrim(cabinet_path, "Xform")
    cabinet_references = cabinet_prim.GetReferences()
    cabinet_references.AddReference('../asset/cabinet.usdz')

    # 櫃子位置調整和旋轉
    cabinet_xform = UsdGeom.Xformable(cabinet_prim)
    cabinet_xform.AddTranslateOp().Set(pos)
    cabinet_xform.AddScaleOp().Set(cabinet_scale)
    cabinet_xform.AddRotateXYZOp().Set(Gf.Vec3d(90, 0, 0))  # 櫃子旋轉 90 度

# 保存 USD 檔案
stage.GetRootLayer().Save()

print("辦公室布局已成功創建：office_layout_updated.usd")
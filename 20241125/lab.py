from pxr import Usd, UsdGeom, Gf

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("20241125/lab.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# 參數設置
x_spacing = 150
z_spacing = 90
table_scale = (1, 1, 1)
cabinet_offset_z = 150
chair_offset_z = -30
computer_height = 110

# 創建桌子的排列
for row in range(5):
    for column in range(4):
        # 計算桌子的座標
        if row in [0, 1]:
            x_position = column * x_spacing
            z_position = row * z_spacing
        elif row in [2, 3]:
            x_position = column * x_spacing
            z_position = (row + 2) * z_spacing
        elif row == 4:
            x_position = column * x_spacing
            z_position = 8 * z_spacing

        position = (x_position, 0, z_position)

        # 創建桌子
        table_name = f"Table_Row{row + 1}_Col{column + 1}"
        table_path = f"/World/{table_name}"
        table_prim = stage.DefinePrim(table_path, "Xform")
        references = table_prim.GetReferences()
        references.AddReference('../asset/table.usdz')

        # 設置旋轉方向
        rotation = 0
        if row in [0, 2]:
            rotation = 180

        # 移動每張桌子到正確位置
        table_xform = UsdGeom.Xformable(table_prim)
        table_xform.AddTranslateOp().Set(position)
        table_xform.AddScaleOp().Set(table_scale)
        table_xform.AddRotateXYZOp().Set(Gf.Vec3d(0, rotation, 0))

        # 添加椅子
        chair_name = f"Chair_Row{row + 1}_Col{column + 1}"
        chair_path = f"/World/{chair_name}"
        chair_prim = stage.DefinePrim(chair_path, "Xform")
        references = chair_prim.GetReferences()
        references.AddReference('../asset/chair.usdz')

        # 根據不同排數設定椅子位置和方向
        if row in [0, 2]:
            chair_position = (x_position, 0, z_position + chair_offset_z)
            chair_rotation = rotation + 180
        else:
            chair_position = (x_position, 0, z_position - chair_offset_z)
            chair_rotation = rotation + 180

        # 設置椅子的位置和旋轉
        chair_xform = UsdGeom.Xformable(chair_prim)
        chair_xform.AddTranslateOp().Set(chair_position)
        chair_xform.AddRotateXYZOp().Set(Gf.Vec3d(0, chair_rotation, 0))

        # 添加電腦
        computer_name = f"Computer_Row{row + 1}_Col{column + 1}"
        computer_path = f"/World/{computer_name}"
        computer_prim = stage.DefinePrim(computer_path, "Xform")
        references = computer_prim.GetReferences()
        references.AddReference('../asset/computer.usdz')

        computer_position = (x_position, computer_height, z_position)
        computer_xform = UsdGeom.Xformable(computer_prim)
        computer_xform.AddTranslateOp().Set(computer_position)
        computer_xform.AddRotateXYZOp().Set(Gf.Vec3d(0, rotation, 0))

# 加入三個櫃子到第五排後面
for i in range(3):
    cabinet_position = (
        i * x_spacing,
        0,
        9 * z_spacing + cabinet_offset_z,
    )

    cabinet_name = f"Cabinet_{i + 1}"
    cabinet_path = f"/World/{cabinet_name}"
    cabinet_prim = stage.DefinePrim(cabinet_path, "Xform")
    references = cabinet_prim.GetReferences()
    references.AddReference('../asset/cabinet.usdz')

    cabinet_xform = UsdGeom.Xformable(cabinet_prim)
    cabinet_xform.AddTranslateOp().Set(cabinet_position)
    cabinet_xform.AddScaleOp().Set((1, 1, 1))
    cabinet_xform.AddRotateXYZOp().Set(Gf.Vec3d(0, 180, 0))

# 保存 USD 檔案
stage.GetRootLayer().Save()

print("場景已成功創建並保留原有物件：lab_move.usd")

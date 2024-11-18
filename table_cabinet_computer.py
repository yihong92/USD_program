from pxr import Usd, UsdGeom, Gf

# 創建新的 USD Stage
stage = Usd.Stage.CreateNew("table_cabinet_computer.usd")

# 設定根層
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# 創建根層物體並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())  # 設定 "/World" 為 default prim

# 參數設置
x_spacing = 100  # 排之間 X 軸的間距
y_spacing = 150  # 每排桌子之間 Y 軸的間距
table_scale = (1, 1, 1)  # 桌子縮放比例 (X, Y, Z)
cabinet_offset_x = 100  # 櫃子與第五排右邊的 X 軸偏移量
cabinet_offset_y = 200  # 櫃子之間的 Y 軸間距
computer_offset = (0, 0, 110)  # 電腦放置在桌子上方的偏移量

# 創建桌子的排列
for row in range(5):  # 共有 5 排
    for column in range(4):  # 每排 4 張桌子
        # 計算桌子的座標
        if row in [0, 1]:  # 第 1 排與第 2 排靠在一起
            x_position = row * x_spacing
            y_position = column * y_spacing
        elif row in [2, 3]:  # 第 3 排與第 4 排靠在一起
            x_position = (row - 2) * x_spacing + 4 * x_spacing
            y_position = column * y_spacing
        else:  # 第 5 排獨立擺放
            x_position = 8 * x_spacing
            y_position = column * y_spacing

        position = (x_position, y_position, 0)

        # 創建容器 Prim 並添加引用桌子
        table_name = f"Table_Row{row + 1}_Col{column + 1}"  # e.g., Table_Row1_Col1, Table_Row2_Col3
        table_path = f"/World/{table_name}"
        table_prim = stage.DefinePrim(table_path, "Xform")  # 創建容器 Prim
        references = table_prim.GetReferences()  # 獲取引用接口
        references.AddReference('asset/table.usd')  # 引用外部桌子資產

        # 移動每張桌子到正確位置
        table_xform = UsdGeom.Xformable(table_prim)
        table_xform.AddTranslateOp().Set(position)
        table_xform.AddScaleOp().Set(table_scale)
        table_xform.AddRotateXYZOp().Set(Gf.Vec3d(0, 0, 0))  # 不旋轉

        # 添加電腦到每排桌子
        if row in [0, 2]:  # 第 1、3 排，正方向擺放
            computer_name = f"Computer_Row{row + 1}_Col{column + 1}"  # e.g., Computer_Row1_Col1
            computer_path = f"/World/{computer_name}"
            computer_prim = stage.DefinePrim(computer_path, "Xform")  # 創建電腦容器 Prim
            references = computer_prim.GetReferences()  # 獲取引用接口
            references.AddReference('asset/computer.usdz')  # 引用外部電腦資產

            # 設定電腦的位置（桌子正上方）
            computer_xform = UsdGeom.Xformable(computer_prim)
            computer_xform.AddTranslateOp().Set((
                position[0] + computer_offset[0],
                position[1] + computer_offset[1],
                position[2] + computer_offset[2]
            ))
            computer_xform.AddScaleOp().Set((1, 1, 1))  # 保持原大小
            computer_xform.AddRotateXYZOp().Set(Gf.Vec3d(90, 0, -90))  # 正方向

        elif row in [1, 3, 4]:  # 第 2、4、5 排，反方向擺放
            computer_name = f"Computer_Row{row + 1}_Col{column + 1}"  # e.g., Computer_Row2_Col1
            computer_path = f"/World/{computer_name}"
            computer_prim = stage.DefinePrim(computer_path, "Xform")  # 創建電腦容器 Prim
            references = computer_prim.GetReferences()  # 獲取引用接口
            references.AddReference('asset/computer.usdz')  # 引用外部電腦資產

            # 設定電腦的位置（桌子正上方）
            computer_xform = UsdGeom.Xformable(computer_prim)
            computer_xform.AddTranslateOp().Set((
                position[0] + computer_offset[0],
                position[1] + computer_offset[1],
                position[2] + computer_offset[2]
            ))
            computer_xform.AddScaleOp().Set((1, 1, 1))  # 保持原大小
            computer_xform.AddRotateXYZOp().Set(Gf.Vec3d(90, 0, 90))  # 反方向

# 加入三個櫃子到第五排右邊
for i in range(3):  # 三個櫃子
    cabinet_position = (
        10 * x_spacing + cabinet_offset_x,  # 櫃子 X 軸位置
        i * cabinet_offset_y,  # 櫃子 Y 軸位置依次遞增
        0,
    )

    cabinet_name = f"Cabinet_{i + 1}"  # e.g., Cabinet_1, Cabinet_2, Cabinet_3
    cabinet_path = f"/World/{cabinet_name}"
    cabinet_prim = stage.DefinePrim(cabinet_path, "Xform")  # 創建櫃子容器 Prim
    references = cabinet_prim.GetReferences()  # 獲取引用接口
    references.AddReference('asset/cabinet.usdz')  # 引用外部櫃子資產

    # 設定櫃子位置和縮放
    cabinet_xform = UsdGeom.Xformable(cabinet_prim)
    cabinet_xform.AddTranslateOp().Set(cabinet_position)
    cabinet_xform.AddScaleOp().Set((1.5, 1.5, 1.5))  # 放大櫃子一點點
    cabinet_xform.AddRotateXYZOp().Set(Gf.Vec3d(90, 0, 270))  # 旋轉到正確方向

# 保存 USD 檔案
stage.GetRootLayer().Save()

print("完整的 USD 場景已成功創建：office_layout_with_all_computers_and_cabinets_v2.usd")
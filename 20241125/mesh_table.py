from pxr import Usd, UsdGeom, Gf

# 创建新的 USD Stage
stage = Usd.Stage.CreateNew("20241125/simple_table_100grid.usd")

# 设置场景的基准（Root）
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 创建根节点
root_prim = stage.DefinePrim("/Root", "Xform")
stage.SetDefaultPrim(root_prim)  # 设置根节点为 Default Prim

# 桌面尺寸 (根据 100x100 Grid)
grid_size = 100
table_top_size = (grid_size * 0.8, grid_size * 0.4)  # 占 Grid 的 80% 长和 40% 宽
table_top_height = grid_size * 0.02  # 桌面厚度比例为 2%

# 创建桌面 (Table Top) 使用内建的平面 (Plane)
table_top_prim = stage.DefinePrim("/Root/TableTop", "Xform")
table_top_geom = UsdGeom.Plane.Define(stage, "/Root/TableTop/Geom")
table_top_geom.AddScaleOp().Set(Gf.Vec3f(table_top_size[0], table_top_height, table_top_size[1]))
table_top_geom.AddTranslateOp().Set(Gf.Vec3f(0, grid_size * 0.5, 0))  # 桌面离地高度为 Grid 高度的 50%

# 桌脚的参数（使用 Cylinder）
leg_height = grid_size * 0.5  # 桌脚高度为 Grid 的 50%
leg_radius = grid_size * 0.02  # 桌脚半径为 Grid 的 2%
leg_offsets = [
    (-table_top_size[0] / 2 + leg_radius, 0, table_top_size[1] / 2 - leg_radius),  # 前左
    (-table_top_size[0] / 2 + leg_radius, 0, -table_top_size[1] / 2 + leg_radius), # 前右
    (table_top_size[0] / 2 - leg_radius, 0, table_top_size[1] / 2 - leg_radius),   # 后左
    (table_top_size[0] / 2 - leg_radius, 0, -table_top_size[1] / 2 + leg_radius)   # 后右
]

# 创建桌脚 (Table Legs) 使用内建的圆柱 (Cylinder)
for i, offset in enumerate(leg_offsets):
    leg_prim_path = f"/Root/TableLeg_{i+1}"
    leg_prim = stage.DefinePrim(leg_prim_path, "Xform")
    leg_geom = UsdGeom.Cylinder.Define(stage, f"{leg_prim_path}/Geom")
    
    # 使用 Get 方法来设置属性
    leg_geom.GetRadiusAttr().Set(leg_radius)
    leg_geom.GetHeightAttr().Set(leg_height)
    leg_geom.AddTranslateOp().Set(Gf.Vec3f(offset[0], leg_height / 2, offset[2]))  # 设置桌脚的位置

# 保存 USD 文件
stage.GetRootLayer().Save()
print("USD 文件 'simple_table_100grid.usd' 已生成，桌子已适配 100x100 Grid")

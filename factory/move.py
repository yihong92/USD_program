import random
from pxr import Usd, UsdGeom, Gf

# 創建新的USD Stage
stage = Usd.Stage.CreateNew("move.usda")

# 設定上軸為Y
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 定義世界根節點並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# 資產路徑
steel_plate_asset_path = "./Steel_Plate.usdz"
forklift_asset_path = "./Forklift.usdz"
truck_asset_path = "./Truck.usdz"
e_tower_asset_path = "./tower.usdz"

# 間距設置
spacing_z = 600.0
plate_thickness = 5.0
min_stack_height = 8
max_stack_height = 12

# 隨機生成 X 間距
def get_random_spacing_x():
    return random.uniform(100.0, 140.0)

# 添加多個 e_tower 在第一排前面
e_tower_base_position = Gf.Vec3f(-400, 0, -300)
num_towers = 3
for i in range(num_towers):
    offset_x = i * 50 + random.uniform(-5, 5)
    offset_z = random.uniform(-10, 10)
    position = e_tower_base_position + Gf.Vec3f(offset_x, 0, offset_z)
    prim_path = f"/World/e_Tower_{i}"
    e_tower_prim = UsdGeom.Xform.Define(stage, prim_path)
    e_tower_prim.GetPrim().SetTypeName('Xform')
    e_tower_prim.GetPrim().GetReferences().AddReference(e_tower_asset_path)
    e_tower_prim.AddTranslateOp().Set(position)

# 添加一個 e_tower 在 x = 500 處
e_tower_500_position = Gf.Vec3f(800, 0, -300)
e_tower_500_prim = UsdGeom.Xform.Define(stage, "/World/e_Tower_500")
e_tower_500_prim.GetPrim().SetTypeName('Xform')
e_tower_500_prim.GetPrim().GetReferences().AddReference(e_tower_asset_path)
e_tower_500_prim.AddTranslateOp().Set(e_tower_500_position)

# 第一排
extra_row_spacing_z = -110.0
x_offset = 0.0
for i in range(7):
    stack_count = random.randint(min_stack_height, max_stack_height)
    for j in range(stack_count):
        position = Gf.Vec3f(x_offset, j * plate_thickness, extra_row_spacing_z)
        prim_path = f"/World/SteelPlate_1_Row_{i}_Stack_{j}"
        prim = UsdGeom.Xform.Define(stage, prim_path)
        prim.GetPrim().SetTypeName('Xform')
        prim.GetPrim().GetReferences().AddReference(steel_plate_asset_path)
        prim.AddTranslateOp().Set(position)
    x_offset += get_random_spacing_x()

# 第二排
x_offset = 0.0
for i in range(7):
    stack_count = random.randint(min_stack_height, max_stack_height)
    for j in range(stack_count):
        position = Gf.Vec3f(x_offset, j * plate_thickness, 0)
        prim_path = f"/World/SteelPlate_2_Row_{i}_Stack_{j}"
        prim = UsdGeom.Xform.Define(stage, prim_path)
        prim.GetPrim().SetTypeName('Xform')
        prim.GetPrim().GetReferences().AddReference(steel_plate_asset_path)
        prim.AddTranslateOp().Set(position)
    x_offset += get_random_spacing_x()

# 添加縮小並旋轉的叉車
forklift_position = Gf.Vec3f(x_offset / 2, 0, spacing_z / 2)
forklift_prim = UsdGeom.Xform.Define(stage, "/World/Forklift")
forklift_prim.GetPrim().SetTypeName('Xform')
forklift_prim.GetPrim().GetReferences().AddReference(forklift_asset_path)
forklift_prim.AddTranslateOp().Set(forklift_position)
forklift_prim.AddScaleOp().Set(Gf.Vec3f(0.3, 0.3, 0.3))

# 動畫相關設置 - 叉車
rotation_frames = 50
move_frames = 150  # 調整為 150 幀，使 X 軸移動更慢
start_rotation = 240.0
end_rotation = 150.0
start_position = forklift_position
end_position_z = forklift_position[2] - 100
end_position_x = forklift_position[0] - 1000

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(rotation_frames + move_frames)

translate_op = forklift_prim.GetOrderedXformOps()[0]
rotate_y_op = forklift_prim.AddRotateYOp()

# 第一階段：旋轉 + 後退（1 到 50 幀）
for frame in range(1, rotation_frames + 1):
    t = (frame - 1) / (rotation_frames - 1)
    rotation_angle = start_rotation + t * (end_rotation - start_rotation)
    z_position = start_position[2] + t * (end_position_z - start_position[2])
    rotate_y_op.Set(rotation_angle, Usd.TimeCode(frame))
    translate_op.Set(Gf.Vec3f(forklift_position[0], forklift_position[1], z_position), Usd.TimeCode(frame))

# 第二階段：緩慢向 -X 移動（51 到 200 幀）
for frame in range(rotation_frames + 1, rotation_frames + move_frames + 1):
    t = (frame - rotation_frames - 1) / (move_frames - 1)
    x_position = start_position[0] + t * (end_position_x - start_position[0])
    translate_op.Set(Gf.Vec3f(x_position, forklift_position[1], end_position_z), Usd.TimeCode(frame))

# 添加卡車到二三排之間右側
truck_scale = 0.1
truck_start_x = x_offset + 50  # 保持 X 軸位置不變（右側）
truck_start_z = spacing_z / 2  # 二三排之間的 Z 軸位置
truck_position = Gf.Vec3f(truck_start_x, 0, truck_start_z)

truck_prim = UsdGeom.Xform.Define(stage, "/World/Truck")
truck_prim.GetPrim().SetTypeName('Xform')
truck_prim.GetPrim().GetReferences().AddReference(truck_asset_path)
truck_prim.AddTranslateOp().Set(truck_position)
truck_prim.AddRotateYOp().Set(180.0)  # 初始翻轉 180 度
truck_prim.AddScaleOp().Set(Gf.Vec3f(truck_scale, truck_scale, truck_scale))

# 動畫相關設置 - 卡車
truck_start_frame = rotation_frames + move_frames + 1
truck_move_z_frames = 50  # 第一階段 X、Z 軸移動和旋轉
truck_move_x_frames = 100  # 第二階段 X 軸移動

truck_end_position_x = truck_start_x - 100  # 第一階段結束的 X 軸位置
truck_end_position_z = truck_start_z - 100  # 第一階段結束的 Z 軸位置
truck_rotate_angle = 90.0  # 第一階段旋轉角度
truck_final_position_x = truck_end_position_x - 1200  # 第二階段結束的 X 軸位置

truck_translate_op = truck_prim.GetOrderedXformOps()[0]
truck_rotate_y_op = truck_prim.GetOrderedXformOps()[1]

# 第一階段：沿 X、Z 軸移動並旋轉（1 到 50 幀）
for frame in range(truck_start_frame, truck_start_frame + truck_move_z_frames):
    t = (frame - truck_start_frame) / (truck_move_z_frames - 1)
    x_position = truck_start_x + t * (truck_end_position_x - truck_start_x)
    z_position = truck_start_z + t * (truck_end_position_z - truck_start_z)
    rotation_angle = 180.0 + t * truck_rotate_angle
    truck_translate_op.Set(Gf.Vec3f(x_position, 0, z_position), Usd.TimeCode(frame))
    truck_rotate_y_op.Set(rotation_angle, Usd.TimeCode(frame))

# 第二階段：沿 X 軸移動 -1200（51 到 150 幀）
for frame in range(truck_start_frame + truck_move_z_frames, truck_start_frame + truck_move_z_frames + truck_move_x_frames):
    t = (frame - truck_start_frame - truck_move_z_frames) / (truck_move_x_frames - 1)
    x_position = truck_end_position_x + t * (truck_final_position_x - truck_end_position_x)
    truck_translate_op.Set(Gf.Vec3f(x_position, 0, truck_end_position_z), Usd.TimeCode(frame))


# 第三排
x_offset = 0.0  # 重置 x_offset，確保第三排從起始位置開始
for i in range(9):
    stack_count = random.randint(min_stack_height, max_stack_height)
    for j in range(stack_count):
        position = Gf.Vec3f(x_offset, j * plate_thickness, spacing_z)
        prim_path = f"/World/SteelPlate_3_Row_{i}_Stack_{j}"
        prim = UsdGeom.Xform.Define(stage, prim_path)
        prim.GetPrim().SetTypeName('Xform')
        prim.GetPrim().GetReferences().AddReference(steel_plate_asset_path)
        prim.AddTranslateOp().Set(position)
    x_offset += get_random_spacing_x()

stage.SetEndTimeCode(truck_start_frame + truck_move_z_frames + truck_move_x_frames)

# 保存USD文件
stage.GetRootLayer().Save()

print("叉車和卡車的動畫已成功生成並保存至 USD 文件。")

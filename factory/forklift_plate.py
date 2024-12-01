import random
from pxr import Usd, UsdGeom, Gf

# 創建新的USD Stage
stage = Usd.Stage.CreateNew("car_plate.usda")

# 設定上軸為Y
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 定義世界根節點並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# 資產路徑
steel_plate_asset_path = "./Steel_Plate.usdz"
forklift_asset_path = "./Forklift.usdz"
truck_asset_path = "./Truck.usdz"

# 間距設置
spacing_z = 600.0  # 排與排之間的Z方向間距
plate_thickness = 5.0  # 每片鋼板的厚度
min_stack_height = 8  # 最小堆疊片數
max_stack_height = 12 # 最大堆疊片數

# 隨機生成 X 間距
def get_random_spacing_x():
    return random.uniform(100.0, 140.0)

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

# 添加縮小並旋轉的叉車（放置於第二排與第三排之間）
forklift_position = Gf.Vec3f(x_offset / 2, 0, spacing_z / 2)
forklift_prim = UsdGeom.Xform.Define(stage, "/World/Forklift")
forklift_prim.GetPrim().SetTypeName('Xform')
forklift_prim.GetPrim().GetReferences().AddReference(forklift_asset_path)
forklift_prim.AddTranslateOp().Set(forklift_position)
forklift_prim.AddScaleOp().Set(Gf.Vec3f(0.3, 0.3, 0.3))
forklift_prim.AddRotateYOp().Set(220.0)

# 添加卡車到第二排右側
truck_scale = 0.15  # 縮小到原大小的 0.15 倍
truck_position = Gf.Vec3f(x_offset + 50, 0, 0)  # 放置在第二排右側，與最後一堆保持距離
truck_prim = UsdGeom.Xform.Define(stage, "/World/Truck")
truck_prim.GetPrim().SetTypeName('Xform')
truck_prim.GetPrim().GetReferences().AddReference(truck_asset_path)
truck_prim.AddTranslateOp().Set(truck_position)
truck_prim.AddScaleOp().Set(Gf.Vec3f(truck_scale, truck_scale, truck_scale))  # 縮小卡車

# 第三排
x_offset = 0.0
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

# 保存USD文件
stage.GetRootLayer().Save()

print("USD 場景已生成並保存為 car_plate.usda。")

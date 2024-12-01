import random
from pxr import Usd, UsdGeom, Gf

# 創建新的USD Stage
stage = Usd.Stage.CreateNew("steel_plate_scene.usda")

# 設定上軸為Y
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# 定義世界根節點並設為 default prim
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# 鐵片資產路徑
steel_plate_asset_path = "./Steel_Plate.usdz"

# 間距設置
spacing_z = 600.0  # 排與排之間的Z方向間距
plate_thickness = 5.0  # 每片鋼板的厚度
min_stack_height = 8  # 最小堆疊片數
max_stack_height = 12 # 最大堆疊片數

# 隨機生成 X 間距
def get_random_spacing_x():
    return random.uniform(100.0, 140.0)

# 第一排（原本的額外排）
extra_row_spacing_z = -110.0
x_offset = 0.0  # 初始 X 偏移
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

# 第二排（原本的第一排）
x_offset = 0.0  # 重置 X 偏移
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

# 第三排（原本的第二排）
x_offset = 0.0  # 重置 X 偏移
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

print("USD 場景已生成並保存為 steel_plate_scene.usda。")

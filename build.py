"""从本地千禧黎明（Millennium Dawn）的中文本地化生成国家全称替换文件。

用法: python build.py [千禧黎明 mod 目录]
默认目录为 Steam 创意工坊 2777392649；千禧黎明更新后重新运行即可同步新国家。
生成结果写入本仓库，并同步到 HOI4 mod 文件夹（MOD_DIR，存在时）。
"""
import re, os, sys, shutil, collections

MD = sys.argv[1] if len(sys.argv) > 1 else r"E:/steam/steamapps/workshop/content/394360/2777392649"
OUT = os.path.dirname(os.path.abspath(__file__))
MOD_DIR = os.path.expanduser(r"~/Documents/Paradox Interactive/Hearts of Iron IV/mod/md_full_country_names")
IDEOS = ["neutrality", "democratic", "fascism", "communism", "nationalist"]

# tag -> official full name (replaces the tag's short name wherever MD uses it)
FULL = {
    # 欧洲
    "ADO": "安道尔公国", "ALB": "阿尔巴尼亚共和国", "AUS": "奥地利共和国", "BEL": "比利时王国",
    "BLR": "白俄罗斯共和国", "BOS": "波斯尼亚和黑塞哥维那", "BUL": "保加利亚共和国", "CRO": "克罗地亚共和国",
    "CYP": "塞浦路斯共和国", "DEN": "丹麦王国", "ENG": "大不列颠及北爱尔兰联合王国", "EST": "爱沙尼亚共和国",
    "FIN": "芬兰共和国", "FRA": "法兰西共和国", "FYR": "马其顿共和国", "GER": "德意志联邦共和国",
    "GRE": "希腊共和国", "HLS": "梵蒂冈城国", "HOL": "荷兰王国", "ITA": "意大利共和国",
    "KOS": "科索沃共和国", "LAT": "拉脱维亚共和国", "LIT": "立陶宛共和国", "LUX": "卢森堡大公国",
    "MLT": "马耳他共和国", "MLV": "摩尔多瓦共和国", "MNC": "摩纳哥公国", "NRY": "挪威王国",
    "POL": "波兰共和国", "POR": "葡萄牙共和国", "SER": "塞尔维亚共和国", "SLO": "斯洛伐克共和国",
    "SLV": "斯洛文尼亚共和国", "SMA": "圣马力诺共和国", "SOV": "俄罗斯联邦", "SPR": "西班牙王国",
    "SWE": "瑞典王国", "SWI": "瑞士联邦", "BAY": "巴伐利亚自由邦", "CAT": "加泰罗尼亚共和国",
    "NCY": "北塞浦路斯土耳其共和国", "PMR": "德涅斯特河沿岸摩尔达维亚共和国", "GGZ": "加告兹共和国",
    "NOV": "新俄罗斯联邦",
    # 高加索 / 俄罗斯联邦主体
    "ABK": "阿布哈兹共和国", "ADJ": "阿扎尔自治共和国", "ARM": "亚美尼亚共和国", "AZE": "阿塞拜疆共和国",
    "NKR": "阿尔察赫共和国", "SOO": "南奥塞梯共和国", "CHE": "车臣伊奇克里亚共和国",
    "ADY": "阿迪格共和国", "ALT": "阿尔泰共和国", "BRY": "布里亚特共和国", "BSH": "巴什科尔托斯坦共和国",
    "CHU": "楚瓦什共和国", "CKK": "楚科奇自治区", "DAG": "达吉斯坦共和国", "ING": "印古什共和国",
    "KAE": "卡累利阿共和国", "KCC": "卡拉恰伊-切尔克斯共和国", "KHM": "汉特-曼西自治区-尤格拉",
    "KHS": "哈卡斯共和国", "KOM": "科米共和国", "MEL": "马里埃尔共和国", "MOV": "莫尔多维亚共和国",
    "NEE": "涅涅茨自治区", "TUV": "图瓦共和国", "UDM": "乌德穆尔特共和国", "YAK": "萨哈（雅库特）共和国",
    "YAM": "亚马尔-涅涅茨自治区", "URA": "乌拉尔共和国",
    # 中亚 / 南亚 / 东亚 / 东南亚
    "AFG": "阿富汗伊斯兰国", "TAL": "阿富汗伊斯兰酋长国", "BAN": "孟加拉人民共和国", "BHU": "不丹王国",
    "BRM": "缅甸联邦共和国", "BRU": "文莱达鲁萨兰国", "CBD": "柬埔寨王国", "CHI": "中华人民共和国",
    "IND": "印度尼西亚共和国", "JAP": "日本国", "KAZ": "哈萨克斯坦共和国", "KOR": "大韩民国",
    "KRP": "卡拉卡尔帕克斯坦共和国", "KYR": "吉尔吉斯共和国", "LAO": "老挝人民民主共和国",
    "MLD": "马尔代夫共和国", "MON": "蒙古国", "NEP": "尼泊尔联邦民主共和国",
    "NKO": "朝鲜民主主义人民共和国", "PAK": "巴基斯坦伊斯兰共和国", "PHI": "菲律宾共和国",
    "RAJ": "印度共和国", "SIA": "泰王国", "SIN": "新加坡共和国", "SRI": "斯里兰卡民主社会主义共和国",
    "TAJ": "塔吉克斯坦共和国", "TIM": "东帝汶民主共和国", "UZB": "乌兹别克斯坦共和国",
    "VIE": "越南社会主义共和国",
    # 中东 / 北非
    "ALG": "阿尔及利亚民主人民共和国", "BHR": "巴林王国", "EGY": "阿拉伯埃及共和国", "IRQ": "伊拉克共和国",
    "ISR": "以色列国", "JOR": "约旦哈希姆王国", "KUW": "科威特国", "LBA": "利比亚国",
    "LEB": "黎巴嫩共和国", "MAU": "毛里塔尼亚伊斯兰共和国", "MOR": "摩洛哥王国", "OMA": "阿曼苏丹国",
    "PAL": "巴勒斯坦国", "PER": "伊朗伊斯兰共和国", "QAT": "卡塔尔国", "SAU": "沙特阿拉伯王国",
    "SHA": "撒拉威阿拉伯民主共和国", "SUD": "苏丹共和国", "SYR": "阿拉伯叙利亚共和国",
    "TUN": "突尼斯共和国", "TUR": "土耳其共和国", "YEM": "也门共和国",
    # 撒哈拉以南非洲
    "AGL": "安哥拉共和国", "BEN": "贝宁共和国", "BOT": "博茨瓦纳共和国", "BUR": "布隆迪共和国",
    "CAM": "喀麦隆共和国", "CDI": "科特迪瓦共和国", "CHA": "乍得共和国", "CNG": "刚果共和国",
    "COM": "科摩罗联盟", "DJI": "吉布提共和国", "EGU": "赤道几内亚共和国", "ERI": "厄立特里亚国",
    "ETH": "埃塞俄比亚联邦民主共和国", "GAB": "加蓬共和国", "GAH": "加纳共和国", "GAM": "冈比亚共和国",
    "GUB": "几内亚比绍共和国", "GUI": "几内亚共和国", "JUB": "朱巴兰州", "KEN": "肯尼亚共和国",
    "LES": "莱索托王国", "LIB": "利比里亚共和国", "MAD": "马达加斯加共和国", "MAL": "马里共和国",
    "MLW": "马拉维共和国", "MOZ": "莫桑比克共和国", "MRT": "毛里求斯共和国", "NAM": "纳米比亚共和国",
    "NGR": "尼日尔共和国", "NIG": "尼日利亚联邦共和国", "PUN": "邦特兰索马里州", "RWA": "卢旺达共和国",
    "SAF": "南非共和国", "SAO": "圣多美和普林西比民主共和国", "SEN": "塞内加尔共和国",
    "SEY": "塞舌尔共和国", "SIE": "塞拉利昂共和国", "SML": "索马里兰共和国", "SOM": "索马里联邦共和国",
    "SSU": "南苏丹共和国", "SWA": "斯威士兰王国", "SWS": "西南索马里州", "TNZ": "坦桑尼亚联合共和国",
    "TOG": "多哥共和国", "UGA": "乌干达共和国", "VER": "佛得角共和国", "ZAM": "赞比亚共和国",
    "ZIM": "津巴布韦共和国", "ANJ": "昂儒昂国",
    # 美洲
    "ARG": "阿根廷共和国", "BAH": "巴哈马国", "BOL": "玻利维亚多民族国", "BRA": "巴西联邦共和国",
    "CHL": "智利共和国", "COL": "哥伦比亚共和国", "COS": "哥斯达黎加共和国", "CUB": "古巴共和国",
    "DMI": "多米尼克国", "ECU": "厄瓜多尔共和国", "ELS": "萨尔瓦多共和国", "GUA": "危地马拉共和国",
    "GUY": "圭亚那合作共和国", "HAI": "海地共和国", "HON": "洪都拉斯共和国", "MEX": "墨西哥合众国",
    "NIC": "尼加拉瓜共和国", "PAN": "巴拿马共和国", "PAR": "巴拉圭共和国", "PRU": "秘鲁共和国",
    "PTR": "波多黎各自由邦", "STK": "圣基茨和尼维斯联邦", "SUR": "苏里南共和国",
    "TRI": "特立尼达和多巴哥共和国", "URG": "乌拉圭东岸共和国", "USA": "美利坚合众国",
    "VEN": "委内瑞拉玻利瓦尔共和国", "CAL": "加利福尼亚共和国", "TEX": "得克萨斯共和国",
    "VMT": "佛蒙特共和国", "RGD": "里奥格兰德共和国", "YUC": "尤卡坦共和国",
    # 大洋洲
    "AST": "澳大利亚联邦", "FIJ": "斐济共和国", "KIR": "基里巴斯共和国", "MAR": "马绍尔群岛共和国",
    "MIC": "密克罗尼西亚联邦", "NAU": "瑙鲁共和国", "PAP": "巴布亚新几内亚独立国", "PAU": "帕劳共和国",
    "SAM": "萨摩亚独立国", "TON": "汤加王国", "VAN": "瓦努阿图共和国",
}

rx = re.compile(r'^\s*([A-Za-z0-9_\.\-]+):\d*\s*"(.*)"\s*(#.*)?$')

def load(path):
    d = collections.OrderedDict()
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = rx.match(line)
            if m:
                d[m.group(1)] = m.group(2)
    return d

base = load(MD + "/localisation/simp_chinese/countries_l_simp_chinese.yml")

def short_of(tag):
    # MD's common short name = neutrality name (fallback: most frequent)
    vals = [base.get(f"{tag}_{i}") for i in IDEOS]
    vals = [v for v in vals if v]
    return base.get(f"{tag}_neutrality") or (collections.Counter(vals).most_common(1)[0][0] if vals else None)

name_key = re.compile(r'^([A-Z0-9]{3})_(.+?)(_DEF)?$')

def transform(d, only_cosmetic=False):
    out = collections.OrderedDict()
    for k, v in d.items():
        if k.endswith("_ADJ") or k.endswith("_desc") or k.endswith("_tt"):
            continue
        m = name_key.match(k)
        if not m:
            continue
        tag = m.group(1)
        new = v
        sh = short_of(tag)
        # 外观标签只替换动态国旗变体（AUTH/AUTH_S/AUTH_SS）和少数确认是同一政权的标签，
        # 其他外观标签（如 BHR_REP 共和国、AZE_PER_STATE 被吞并）可能代表不同政体，不套用全称
        cos_ok = (not only_cosmetic) or re.match(r'^[A-Z0-9]{3}_(AUTH(_S|_SS)?|burma|serbia_tag|social_democrat)(_|$)', k)
        if tag in FULL and sh and v == sh and cos_ok:
            new = FULL[tag]
        # DEF that is a truncated form of its name (e.g. 远东 vs 远东共和国)
        if m.group(3):
            nm = d.get(k[:-4])
            nm = out.get(k[:-4], nm)
            if nm and nm != new and nm.startswith(new) and len(nm) > len(new):
                new = nm
        if new != v:
            out[k] = new
    return out

changes = transform(base)
cos_path = MD + "/localisation/simp_chinese/MD_countries_cosmetic_l_simp_chinese.yml"
cos = load(cos_path)
cos_changes = transform(cos, only_cosmetic=True)
for k in list(cos_changes):
    if k in changes:
        del cos_changes[k]

os.makedirs(OUT + "/localisation/simp_chinese/replace", exist_ok=True)

def write(path, header, items):
    with open(path, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write("l_simp_chinese:\n")
        f.write(f" # {header}\n")
        for k, v in items.items():
            f.write(f' {k}: "{v}"\n')

write(OUT + "/localisation/simp_chinese/replace/zz_md_full_country_names_l_simp_chinese.yml",
      "千禧黎明 国家全称 - 基础国家名", changes)
write(OUT + "/localisation/simp_chinese/replace/zz_md_full_country_names_cosmetic_l_simp_chinese.yml",
      "千禧黎明 国家全称 - 外观标签（动态国旗等）", cos_changes)

tags_changed = sorted({k[:3] for k in changes} | {k[:3] for k in cos_changes})
print("base keys", len(changes), "cosmetic keys", len(cos_changes), "tags", len(tags_changed))

# 同步到游戏 mod 文件夹；descriptor.mod 不覆盖，以保留启动器写入的 remote_file_id
if os.path.isdir(MOD_DIR):
    shutil.copytree(OUT + "/localisation", MOD_DIR + "/localisation", dirs_exist_ok=True)
    shutil.copy2(OUT + "/thumbnail.png", MOD_DIR)
    print("synced to", MOD_DIR)

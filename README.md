# 千禧黎明 国家全称 | MD Full Country Names (CN)

钢铁雄心4「千禧黎明」（Millennium Dawn）的简体中文子 mod：把游戏里的国家简称替换为正式全称。

| 原版 | 本 mod |
|---|---|
| 中国 | 中华人民共和国 |
| 美国 | 美利坚合众国 |
| 联合王国 | 大不列颠及北爱尔兰联合王国 |
| 俄罗斯 | 俄罗斯联邦 |
| 伊朗 | 伊朗伊斯兰共和国 |

## 特点

- 覆盖 220+ 个国家，所有意识形态的国名和 `_DEF`（句中称呼）都会替换。
- 形容词（`_ADJ`，如"中国的"）保持不变，避免出现"中华人民共和国陆军"之类的说法。
- 千禧黎明已经为某些意识形态起了专门名字的（如"阿富汗伊斯兰酋长国"），不会被覆盖。
- 动态国旗变体（`TAG_AUTH` / `_AUTH_S` / `_AUTH_SS` 等外观标签）同步替换；代表不同政体的外观标签不动。
- 文件放在 `localisation/simp_chinese/replace/`，只覆盖改动的键，千禧黎明更新新增国家时不会冲突。

## 安装

推荐在 Steam 创意工坊订阅：<https://steamcommunity.com/sharedfiles/filedetails/?id=3815035583>

手动安装：

1. 把 `descriptor.mod`、`thumbnail.png` 和 `localisation` 文件夹复制到 `文档/Paradox Interactive/Hearts of Iron IV/mod/md_full_country_names`。
2. 在 `mod` 目录下新建 `md_full_country_names.mod`，内容为 `descriptor.mod` 的内容加上一行：
   ```
   path="C:/Users/<你的用户名>/Documents/Paradox Interactive/Hearts of Iron IV/mod/md_full_country_names"
   ```
3. 在启动器的播放集里启用，排在千禧黎明之后。

> 不要和旧的同类 mod（创意工坊 3239046193，1.15 版）同时启用。

## 千禧黎明更新后重新生成

```bash
python build.py "E:/steam/steamapps/workshop/content/394360/2777392649"
```

参数是千禧黎明 mod 所在目录（创意工坊 ID 2777392649），省略时使用脚本里的默认路径。要调整某个国家的译名，修改 `build.py` 里的 `FULL` 表后重新运行。生成结果会同时同步到上面的 HOI4 mod 文件夹（如果存在），之后在启动器里更新创意工坊即可。

封面图由 `tools/make_thumbnail.py` 生成。

## 译名规则

- 一般使用现行正式全称（如 玻利维亚多民族国、缅甸联邦共和国）。
- 简称沿用千禧黎明的叫法，全称与之对应（如"马其顿"→马其顿共和国、"斯威士兰"→斯威士兰王国）。
- 阿富汗按 2000 年开局：北方联盟（AFG）为阿富汗伊斯兰国，塔利班（TAL）为阿富汗伊斯兰酋长国。
- 正式名称即简称的（加拿大、乌克兰、匈牙利等）、组织和武装、没有真实全称的架空分裂国家，保持原样。

## 许可证

[Apache-2.0](LICENSE)

# eva_gos_2nd_pc
This project is intended to make an unofficial Chinese translation to the visual novel game `Evangelion: Girlfriend of Steel 2nd` PC edition (AKA Iron Maiden 2nd).
本项目为游戏`新世纪福音战士：钢铁女友2nd`PC版的非官方汉化。如有建议欢迎提出。

修改日志：
- 2025/09/26 项目1.0版发布。仅汉化文本。

使用方法：下载`chinese-patch-1.0.zip`并解压，将`exec.idx`、`exec.lb5`复制到游戏目录下替换原文件（建议预先备份），将`test03-cn.exe`复制到游戏目录下`exe`文件夹中双击启动即可。

汉化说明：

汉化文本翻译最初来源于EVA同好会，经B站@main_void大佬调整，PSP版发布于https://tieba.baidu.com/p/9527348639 ，汉化文本发布于 https://paratranz.cn/projects/13612 ，再由本人针对PC版进行进一步微调。如有不妥请联系本人。

全部文本翻译内容置于`translation_map.json`中，该文件为调用paratranz API读取上述项目生成后再手工调整，调整内容包括：
- 日文PC版原文与PSP版有出入的地方，将origin和key项均改为PC版内容（吐槽下这一项最为麻烦，谁能想到这俩文本还能不一样呢，PC版文本相比PSP版经常在某些地方多加一个句号，或者多加一个假名，或者是多加或删去换行符，或者是用了同音字，或者是有些商店名称不同）；
- 偶见翻译错别字修正；
- 翻译歧义调整（本人并不懂日语，借助网络翻译及个人理解调整了一两句）；
- PSP版未收录的文本项在末尾单独添加，单独添加的条目仅有origin和translation项。

以上调整的具体内容本人未作完整记录（原谅我不是专业程序员，并不会版本控制什么的）。

汉化工作几乎完全依赖于GOS2-Tools的使用（ https://github.com/Durik256/GOS2-Tools ），该工具提供了钢铁女友2nd文本、图片、语音资源解包及打包的完全解决方案。得知该工具是通过钢铁女友2nd的PC英化版（ https://pearsehillock.blogspot.com/2015/08/neon-genesis-evangelion-girlfriend-of_7.html ）。

通过解包发现游戏PC版目录下的`event`为bmp格式的场景及事件CG打包，`exec`为txt格式的游戏流程控制代码打包（包括全部文本），`imgfrm`为bmp格式的系统界面图片打包。针对`exec`解包得到的txt文件，编写python脚本根据`translation_map.json`替换后再打包即可。

英化工作只需替换上述文件即可，而汉化还要进行的一步（当然也是常见的一步）是文字编码处理。游戏的可执行文件`test03.exe`默认采用shift-jis编码读取文本，为读取中文文本需要改为gbk编码。采用Ollydbg对该文件进行反编译，找到`CreateFontIndirectA`函数并将传入编码参数改为0x86，然后将所有用于判断字符编码边界的`cmp al 9F`命令中的9F改为FE。学习来源： https://www.bilibili.com/opus/556226946625153023 、 https://www.cnblogs.com/bl4nk/archive/2011/07/17/2909131.html 、 https://bbs.kanxue.com/thread-260061-1.htm 等。

免责声明：游戏`新世纪福音战士：钢铁女友2nd`版权属于GAINAX。本项目仅为个人学习使用，禁止用于商业，本人不对因使用该汉化项目而产生的一切直接或间接后果承担任何责任。

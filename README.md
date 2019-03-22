# vtb
本程序主要是为了
1.爬取某个/某些UP的信息与旗下发布视频的信息
2.爬取某个标签中的视频信息

getUserAndVideoInfo 爬取VTBList 中的UPID列表，获得UP的信息和发布视频的信息（粗略的）

listread 读取文件LIST

scheduleInfo 修改进度表，用来达成断点续传的效果

tagSearch 爬取某个 TAG 下的所有视频的UP 并写入到VTBList

userInfo 查询/插入 UP主信息

videoInfo 查询/插入 视频信息

userVtbVideoCount 获得UP视频中与VTB相关视频的数量

videoDetailInfo 通过视频ID获得视频详细信息

videoTagCut 用来将爬取出的TAG从一个字符串分割成单项并存入表中

videoTagInfo 爬取TAG信息 给videoTagCut 用

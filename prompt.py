SYSTEM_PROMPT = """请你直接给出顾客的评论文本在18个评论维度上分在别表现出了怎么样的情感倾向：

---
# 18个细分评论维度由5个粗粒度的维度获得：

位置：
- Location#Transportation；餐厅的交通便利程度,主要是指交通工具的易到达程度；
- Location#Downtown；餐厅地理位置、分布；
- Location#Easy_to_find：主要指餐厅是否容易寻找，与地理位置无关；

服务：
- Service#Queue；餐厅排队情况、用餐人数等；
- Service#Hospitality；餐厅服务人员态度；
- Service#Parking；餐厅附近停车的便利程度；
- Service#Timely：餐厅服务的及时性；

价格：
- Price#Level；餐厅的价格水平；
- Price#Cost_effective；餐厅性价比；
- Price#Discount：餐厅折扣力度与活动优惠情况；

环境：
- Ambience#Decoration；餐厅装修情况；
- Ambience#Noise；餐厅嘈杂情况；
- Ambience#Space；就餐空间大小情况；
- Ambience#Sanitary：卫生情况；

食物：
- Food#Portion；食物分量情况；
- Food#Taste；食物口味情况；
- Food#Appearance；食物外观；
- Food#Recommendation：对餐厅的推荐程度；

# 情感倾向分为：负面：-1；中性或未提及对应的评论维度：0；正面：1
---
现在请你开始进行情感倾向判断，直接输出对应18个评论维度的情感倾向，例如

Input: 这家店的位置很是好找，就在鼓楼南门正对面。环境很好，有空调也有免费的无线网，空间很大，很多位置每个位置的分布也很是很好，经常来吃了，但是口味有点偏咸！感觉汤是酱油兑出来的，不是很鲜，每次想和服务员说的但都忘了。上菜速度也是很快，服务也很是周到，不管人多人少，总是给人一种舒适的感觉，很是喜欢在此用餐。食材里应该都是速冻食品，所以吃起来觉得不是很新鲜，不过不是很影响主要口味。还有一点就是米线的分量有点少了，没有别家的多，如果再加一份的话要五块钱，价格稍微有点偏贵了。
Output: Location#Transportation: 0, Location#Downtown: 0, Location#Easy_to_find: 1, Service#Queue: 0, Service#Hospitality: 1, Service#Parking: 0, Service#Timely: 1, Price#Level: -1, Price#Cost_effective: 0, Price#Discount: 0, Ambience#Decoration: 1, Ambience#Noise: 1, Ambience#Space: 1, Ambience#Sanitary: 1, Food#Portion: 0, Food#Taste: 1, Food#Appearance: 0, Food#Recommendation: 0

---
现在，请你开始进行分类。
Input：{question}"""